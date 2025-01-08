# Walker - Directory Analysis Tool

Walker is a Python utility that helps analyze and document directory structures. It provides two main functions:

1. **Directory Tree Generation**: Creates a markdown file showing the complete directory structure
2. **File Combination**: Combines all files from a directory into a single markdown document

## Features

- Generates clean, formatted markdown output
- Handles both text and binary files
- Preserves file hierarchy in combined output
- Includes syntax highlighting for code files
- Provides detailed error handling and reporting

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/walker.git
cd walker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Generate Directory Tree
```bash
python walker.py /path/to/directory --tree
```

### Combine Files
```bash
python walker.py /path/to/directory
```

### Options
- `-o` or `--output`: Specify output file name
- `--tree`: Generate directory tree instead of combining files

## Examples

1. Generate directory tree with custom output file:
```bash
python walker.py /path/to/directory --tree -o my_tree.md
```

2. Combine files with default output:
```bash
python walker.py /path/to/directory
```

## Output Format

### Directory Tree
- Uses ASCII art for tree structure
- Includes generation timestamp
- Shows absolute path of source directory

### Combined Files
- Each file is separated by markdown headers
- Includes syntax highlighting based on file extension
- Handles binary files gracefully
- Preserves relative paths in output

## Requirements

- Python 3.6+
- Standard library modules only (no external dependencies)

## Acknowledgements

This project was originally inspired by:
- [Original source code on Pastebin](https://pastebin.com/KT8icTMv)
- [Reddit discussion thread](https://www.reddit.com/r/ChatGPTCoding/comments/1hinwsr/the_goat_workflow/)

## License

MIT License - See LICENSE file for details