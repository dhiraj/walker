# Walker - Directory Analysis Tool

Walker is a Python utility that helps analyze and document directory structures. It provides two main functions:

1. **Directory Tree Generation**: Creates a markdown file showing the complete directory structure
2. **File Combination**: Combines all files from a directory into a single markdown document with syntax highlighting

## Features

- Generates clean, formatted markdown output
- Automatically skips common directories (`.git`, `node_modules`, `__pycache__`, etc.) and file types (images, binaries, archives)
- Handles multiple text encodings (UTF-8, UTF-16, Latin-1, CP1252)
- Uses mimetypes to identify text files
- Includes syntax highlighting for code files
- Optional inclusion of hidden files and directories
- Optional display of file sizes
- Configurable file exclusion patterns
- Maximum file size limits for large file handling
- Comprehensive error handling and logging
- Verbose logging option for debugging

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dhiraj/walker.git
cd walker
```

2. No external dependencies required - uses only Python standard library.

## Usage

### Basic Usage
```bash
# Combine files (default command)
python walker.py [directory]

# Generate directory tree
python walker.py tree [directory]
```

### Commands

- `combine` (default): Combine all files into a single markdown document
- `tree`: Generate directory tree structure only

### Options

#### Global Options
- `-v, --verbose`: Enable verbose logging
- `-o, --output FILE`: Specify output file name (default: `combined_output.md` for combine, `file_tree.md` for tree)
- `--hidden`: Include hidden files and directories
- `--sizes`: Show file sizes in the tree output
- `directory`: Directory path to process (default: current directory)

#### Combine Command Options
- `--exclude EXT [EXT ...]`: Additional file extensions to exclude (e.g., `.log .tmp`)
- `--max-size SIZE`: Maximum file size in bytes to include
- `--no-toc`: Disable table of contents generation

## Examples

### Generate Directory Tree
```bash
# Basic tree
python walker.py tree /path/to/project

# Tree with file sizes and hidden files
python walker.py tree /path/to/project --sizes --hidden -o project_tree.md
```

### Combine Files
```bash
# Basic combine (default)
python walker.py /path/to/project

# Combine with exclusions and size limit
python walker.py combine /path/to/project --exclude .log .tmp --max-size 1048576 -o project_docs.md

# Combine including hidden files, verbose output
python walker.py /path/to/project --hidden --verbose
```

## Output Format

### Directory Tree Output
- ASCII art tree structure with proper indentation
- Generation timestamp and source directory path
- Optional file sizes in bytes
- Skips common directories by default

### Combined Files Output
- Markdown header for each file showing relative path
- Syntax highlighting based on file extension
- Table of contents with file links
- Directory tree overview at the top
- Graceful handling of unreadable files
- File count summary
- Generation timestamp

## Default Exclusions

### Skipped Directories
`.git`, `node_modules`, `__pycache__`, `.next`, `.nuxt`, `dist`, `build`, `venv`, `.venv`, `docs`

### Skipped File Extensions
Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.ico`, `.svg`  
Binaries: `.exe`, `.dll`, `.so`, `.dylib`, `.bin`, `.dat`, `.db`, `.sqlite`, `.sqlite3`  
Archives: `.zip`, `.tar`, `.gz`, `.bz2`, `.rar`, `.7z`  
Media: `.mp3`, `.mp4`, `.avi`, `.mkv`, `.flv`, `.wmv`, `.mov`, `.webm`  
Documents: `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`  
Compiled: `.pyc`, `.class`, `.jar`, `.war`, `.ear`

### Skipped Specific Files
`tailwind.css`, `uv.lock`

## Requirements

- Python 3.6+
- Standard library modules only (no external dependencies)

## Error Handling

- Permission errors are logged and skipped
- Unreadable files are marked in output
- Large files can be excluded with `--max-size`
- Multiple encoding attempts for text files
- Comprehensive logging with verbose option

## Acknowledgements

This project was originally inspired by:
- [Original source code on Pastebin](https://pastebin.com/KT8icTMv)
- [Reddit discussion thread](https://www.reddit.com/r/ChatGPTCoding/comments/1hinwsr/the_goat_workflow/)

## License

MIT License - See LICENSE file for details
