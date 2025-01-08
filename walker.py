#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


def generate_tree(directory_path, output_file="file_tree.md"):
    """
    Generates a markdown file containing the directory/file tree structure.
    """
    try:
        # Convert to absolute path and verify directory exists
        abs_path = os.path.abspath(directory_path)
        if not os.path.isdir(abs_path):
            print(f"Error: '{directory_path}' is not a valid directory")
            return False

        # Create or truncate output file
        with open(output_file, "w", encoding="utf-8") as outfile:
            # Write header with timestamp
            outfile.write(f"# Directory Tree Report\n\n")
            outfile.write(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            outfile.write(f"Source directory: `{directory_path}`\n\n")
            outfile.write("```\n")

            # Walk through directory recursively
            for root, dirs, files in os.walk(abs_path):
                # Calculate depth for indentation
                level = root.replace(abs_path, "").count(os.sep)
                indent = "│   " * level

                # Print directory name
                dir_name = os.path.basename(root)
                if level == 0:
                    outfile.write(f"{dir_name}/\n")
                else:
                    outfile.write(f"{indent}├── {dir_name}/\n")

                # Print files
                subindent = "│   " * (level + 1)
                for i, file in enumerate(sorted(files)):
                    if i == len(files) - 1 and not dirs:  # Last file in directory
                        outfile.write(f"{subindent[:-4]}└── {file}\n")
                    else:
                        outfile.write(f"{subindent}├── {file}\n")

            outfile.write("```\n")
            outfile.write("\n# End of Directory Tree Report\n")

        print(f"Successfully generated directory tree in '{output_file}'")
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def combine_files(directory_path, output_file="combined_output.md"):
    """
    Recursively combines all files from the given directory into a single markdown file.
    Each file's content is formatted with markdown syntax for better readability.
    """
    try:
        # Convert to absolute path and verify directory exists
        abs_path = os.path.abspath(directory_path)
        if not os.path.isdir(abs_path):
            print(f"Error: '{directory_path}' is not a valid directory")
            return False

        # Create or truncate output file
        with open(output_file, "w", encoding="utf-8") as outfile:
            # Write header with timestamp
            outfile.write(f"# Combined Files Report\n\n")
            outfile.write(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            outfile.write(f"Source directory: `{directory_path}`\n\n")
            outfile.write("---\n\n")

            # Walk through directory recursively
            for root, _, files in os.walk(abs_path):
                for filename in sorted(files):
                    # Skip the output file itself if it's in the directory
                    if filename == output_file:
                        continue

                    file_path = os.path.join(root, filename)

                    # Calculate relative path from the input directory
                    rel_path = os.path.relpath(file_path, abs_path)

                    try:
                        # Try to read the file as text
                        with open(file_path, "r", encoding="utf-8") as infile:
                            # Write file header with path
                            outfile.write(f"## {rel_path}\n\n")

                            # Determine language for syntax highlighting based on file extension
                            ext = os.path.splitext(filename)[1].lstrip(".")
                            if ext:
                                outfile.write(f"```{ext}\n")
                            else:
                                outfile.write("```\n")

                            # Write file contents
                            outfile.write(infile.read())
                            outfile.write("\n```\n\n")

                            # Add separator between files
                            outfile.write("---\n\n")
                    except UnicodeDecodeError:
                        # Handle binary files
                        outfile.write(f"## {rel_path}\n\n")
                        outfile.write("*[Binary file]*\n\n")
                        outfile.write("---\n\n")
                    except Exception as e:
                        # Log other errors but continue processing
                        outfile.write(f"## {rel_path}\n\n")
                        outfile.write(f"*[Error reading file: {str(e)}]*\n\n")
                        outfile.write("---\n\n")

            # Write footer
            outfile.write("# End of Combined Files Report\n")

        print(f"Successfully combined files into '{output_file}'")
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Combine files or generate directory tree structure."
    )
    parser.add_argument("directory", help="Directory path to process")
    parser.add_argument("-o", "--output", help="Output file name", default=None)
    parser.add_argument(
        "--tree",
        action="store_true",
        help="Generate directory tree instead of combining files",
    )

    args = parser.parse_args()

    if args.tree:
        output_file = args.output if args.output else "file_tree.md"
        if not generate_tree(args.directory, output_file):
            sys.exit(1)
    else:
        output_file = args.output if args.output else "combined_output.md"
        if not combine_files(args.directory, output_file):
            sys.exit(1)


if __name__ == "__main__":
    main()