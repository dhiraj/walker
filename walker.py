#!/usr/bin/env python3
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Set, List
from datetime import datetime
import mimetypes
import os

# Central lists for skipping directories and file extensions
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.next', '.nuxt', 'dist', 'build', 'venv', '.venv', 'docs'}
SKIP_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.svg',
                   '.exe', '.dll', '.so', '.dylib', '.bin', '.dat', '.db', '.sqlite', '.sqlite3',
                   '.zip', '.tar', '.gz', '.bz2', '.rar', '.7z',
                   '.mp3', '.mp4', '.avi', '.mkv', '.flv', '.wmv', '.mov', '.webm',
                   '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                   '.pyc', '.class', '.jar', '.war', '.ear'}
SKIP_FILES = {'tailwind.css', 'uv.lock'}  # Skip specific minified or unwanted files


def _build_tree(
    path: Path,
    prefix: str = "",
    is_last: bool = True,
    show_hidden: bool = False,
    show_sizes: bool = False,
    skip_dirs: Optional[Set[str]] = None
) -> List[str]:
    """
    Recursively build tree lines for the directory.

    Args:
        path: Current directory path
        prefix: Current prefix string
        is_last: Whether this is the last item in its level
        show_hidden: Include hidden files/directories
        show_sizes: Show file sizes
        skip_dirs: Set of directory names to skip

    Returns:
        List of tree lines
    """
    lines = []
    indent = prefix + ("└── " if is_last else "├── ")
    lines.append(indent + path.name + "/")

    # Get children with optional filtering
    try:
        children = list(path.iterdir())
    except PermissionError:
        logging.warning(f"Permission denied: {path}")
        return lines

    if skip_dirs:
        children = [c for c in children if show_hidden or not c.name.startswith('.')]
        dirs = sorted([c for c in children if c.is_dir() and c.name not in skip_dirs])
        files = sorted([c for c in children if c.is_file()])
    else:
        children = [c for c in children if show_hidden or not c.name.startswith('.')]
        dirs = sorted([c for c in children if c.is_dir()])
        files = sorted([c for c in children if c.is_file()])

    # Update prefix for next level
    sub_prefix = prefix + ("    " if is_last else "│   ")

    # Process subdirs
    for i, dir_path in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1 and not files)
        lines.extend(_build_tree(
            dir_path,
            sub_prefix,
            is_last_dir,
            show_hidden,
            show_sizes,
            skip_dirs
        ))

    # Process files
    for i, file_path in enumerate(files):
        is_last_file = (i == len(files) - 1)
        indent_file = sub_prefix + ("└── " if is_last_file else "├── ")
        file_name = file_path.name
        if show_sizes:
            try:
                size = file_path.stat().st_size
                size_str = f" ({size} bytes)"
            except OSError:
                size_str = " (size unknown)"
            file_name += size_str
        lines.append(indent_file + file_name)

    return lines


def generate_tree(
    directory_path: str,
    output_file: str = "file_tree.md",
    show_hidden: bool = False,
    show_sizes: bool = False
) -> bool:
    """
    Generates a markdown file containing the directory/file tree structure.

    Args:
        directory_path: Path to the directory to process
        output_file: Output markdown file path
        show_hidden: Include hidden files and directories
        show_sizes: Show file sizes in the tree

    Returns:
        True if successful, False otherwise
    """
    try:
        abs_path = Path(directory_path).resolve()
        if not abs_path.is_dir():
            logging.error(f"'{directory_path}' is not a valid directory")
            return False

        with open(output_file, "w", encoding="utf-8") as outfile:
            # Write header
            outfile.write("# Directory Tree Report\n\n")
            outfile.write(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            outfile.write(f"Source directory: `{directory_path}`\n\n")
            outfile.write("```\n")

            # Build tree
            tree_lines = _build_tree(abs_path, show_hidden=show_hidden, show_sizes=show_sizes)
            outfile.write("\n".join(tree_lines))

            outfile.write("\n```\n\n# End of Directory Tree Report\n")

        logging.info(f"Successfully generated directory tree in '{output_file}'")
        return True

    except Exception as e:
        logging.error(f"Error generating tree: {str(e)}")
        return False


def _read_file_with_fallback(file_path: Path, encodings: Optional[List[str]] = None) -> Optional[str]:
    """
    Attempt to read a file with multiple encodings.

    Args:
        file_path: Path to the file
        encodings: List of encodings to try, defaults to utf-8, latin-1, cp1252

    Returns:
        File content as string if successful, None if failed
    """
    if encodings is None:
        encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']

    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception:
            return None
    return None


def _is_text_file(file_path: Path) -> bool:
    """
    Check if file is likely a text file using mimetypes.

    Args:
        file_path: Path to the file

    Returns:
        True if likely text, False otherwise
    """
    mime_type, _ = mimetypes.guess_type(file_path.name)
    if mime_type:
        return mime_type.startswith('text/')
    # Default to text for files without extension (common for scripts like LICENSE, Makefile)
    if not file_path.suffix:
        return True
    # Default to text for common extensions
    text_exts = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.csv', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd', '.make', '.cmake', '.toml', '.ini', '.cfg', '.conf', '.env', '.lock', '.sum', '.go', '.rs', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.php', '.rb', '.pl', '.lua', '.swift', '.kt', '.scala', '.clj', '.hs', '.ml', '.fs', '.elm', '.dart', '.ex', '.exs', '.vb', '.fs', '.nim', '.cr'}
    return file_path.suffix.lower() in text_exts


def combine_files(
    directory_path: str,
    output_file: str = "combined_output.md",
    exclude_patterns: Optional[Set[str]] = None,
    max_size: Optional[int] = None,
    show_hidden: bool = False,
    include_toc: bool = True,
    show_sizes: bool = False
) -> bool:
    """
    Recursively combines all files from the given directory into a single markdown file.

    Args:
        directory_path: Path to the directory to process
        output_file: Output markdown file path
        exclude_patterns: Set of file extensions to exclude (e.g., {'.jpg', '.exe'})
        max_size: Maximum file size in bytes to include
        show_hidden: Include hidden files
        include_toc: Generate table of contents

    Returns:
        True if successful, False otherwise
    """
    try:
        logging.debug(f"combine_files called with directory_path={repr(directory_path)}, output_file={repr(output_file)}, exclude_patterns={repr(exclude_patterns)}")
        abs_path = Path(directory_path).resolve()
        if not abs_path.is_dir():
            logging.error(f"'{directory_path}' is not a valid directory")
            return False

        if exclude_patterns is None:
            exclude_patterns = set()

        # Collect all files
        all_files = []
        for root, dirs, files in os.walk(abs_path):
            rel_root = Path(root).relative_to(abs_path)
            # Filter dirs to skip SKIP_DIRS
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for file in files:
                rel_file_path = rel_root / file
                if not show_hidden and (rel_file_path.name.startswith('.') or any(p.startswith('.') for p in rel_root.parts)):
                    continue
                if rel_file_path.name in SKIP_FILES:
                    continue
                if rel_file_path.suffix.lower() in exclude_patterns:
                    continue
                # Skip minified files
                if ".min." in rel_file_path.name:
                    continue
                abs_file_path = abs_path / rel_file_path
                if max_size and abs_file_path.stat().st_size > max_size:
                    logging.info(f"Skipping large file: {abs_file_path} ({abs_file_path.stat().st_size} bytes)")
                    continue
                if not _is_text_file(abs_file_path):
                    continue
                all_files.append(rel_file_path)

        # Sort files
        all_files.sort()

        with open(output_file, "w", encoding="utf-8") as outfile:
            # Write header
            outfile.write("# Combined Files Report\n\n")
            outfile.write(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            outfile.write(f"Source directory: `{directory_path}`\n\n")
            outfile.write(f"Total files processed: {len(all_files)}\n\n")

            # Directory Tree
            outfile.write("## Directory Tree\n\n")
            outfile.write("```\n")
            tree_lines = _build_tree(abs_path, show_hidden=show_hidden, show_sizes=False, skip_dirs=SKIP_DIRS)
            outfile.write("\n".join(tree_lines))
            outfile.write("\n```\n\n")

            # Process each file
            for i, rel_file_path in enumerate(all_files):
                abs_file_path = abs_path / rel_file_path

                # Skip output file
                try:
                    abs_file_path = abs_file_path.resolve()
                except OSError:
                    logging.warning(f"Could not resolve path: {abs_file_path}")
                    continue

                if abs_file_path == Path(output_file).resolve():
                    continue

                anchor = str(rel_file_path).replace('/', '_').replace('.', '_')
                outfile.write(f"## {rel_file_path}\n\n")

                content = _read_file_with_fallback(abs_file_path)
                if content is not None:
                    # Syntax highlighting
                    ext = rel_file_path.suffix.lstrip('.')
                    lang = ext or 'text'
                    outfile.write(f"```{lang}\n{content}\n```\n\n")
                    if i < len(all_files) - 1:
                        outfile.write("---\n\n")
                else:
                    outfile.write("*[Unreadable file]*\n\n")

            outfile.write("# End of Combined Files Report\n")

        logging.info(f"Successfully combined files into '{output_file}'")
        return True

    except Exception as e:
        logging.error(f"Error combining files: {str(e)}")
        return False


def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
        stream=sys.stderr
    )

    parser = argparse.ArgumentParser(
        description="Combine files or generate directory tree structure. Default command is 'combine'.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument(
        "--hidden",
        action="store_true",
        help="Include hidden files and directories"
    )
    parser.add_argument(
        "--sizes",
        action="store_true",
        help="Show file sizes in the tree"
    )
    parser.add_argument("directory", nargs='?', default=".", help="Directory path to process (default: current directory)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Tree command
    tree_parser = subparsers.add_parser(
        "tree",
        help="Generate directory tree",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Combine command
    combine_parser = subparsers.add_parser(
        "combine",
        help="Combine files into single markdown",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    combine_parser.add_argument(
        "--exclude",
        nargs="+",
        default=[],
        help="File extensions to exclude (e.g., .jpg .exe)"
    )
    combine_parser.add_argument(
        "--max-size",
        type=int,
        help="Maximum file size in bytes to include"
    )
    combine_parser.add_argument(
        "--no-toc",
        action="store_true",
        help="Disable table of contents"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.command is None:
        args.command = "combine"

    if args.command == "tree":
        success = generate_tree(
            args.directory,
            args.output or 'file_tree.md',
            show_hidden=getattr(args, 'hidden', False),
            show_sizes=getattr(args, 'sizes', False)
        )
    elif args.command == "combine":
        exclude_set = SKIP_EXTENSIONS.copy()
        if hasattr(args, 'exclude') and args.exclude:
            exclude_set |= {ext if ext.startswith('.') else f'.{ext}' for ext in args.exclude}
        success = combine_files(
            args.directory,
            args.output or 'combined_output.md',
            exclude_patterns=exclude_set,
            max_size=getattr(args, 'max_size', None),
            show_hidden=getattr(args, 'hidden', False),
            include_toc=not getattr(args, 'no_toc', False),
            show_sizes=getattr(args, 'sizes', False)
        )
    else:
        parser.error(f"Unknown command: {args.command}")
        success = False

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
