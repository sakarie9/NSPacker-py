# NSPacker-py

English | [中文](./README.md)

NSPacker-py is a command-line tool for handling Nintendo Switch game package files (NSP). This tool can unpack, edit, and repack NSP files.

## Features

- **Extract NSP files**: Unpack NSP files
- **Edit NSP information**: Modify game title ID, name, author, and version information
- **Pack NCA files**: Repack edited content into NSP files

## Installation

```bash
git clone https://github.com/yourusername/nspacker-py.git
cd nspacker-py
```

## Usage

### Binary Requirements

This script calls external binary files to simplify the code.

Before using, you need to place the required files in the same directory as `main.py`, or in a directory included in your `PATH` environment variable.

> [!IMPORTANT]
> Missing `nstool` and `hactoolnet` will prevent unpacking.

> [!IMPORTANT]
> Missing `hacpack` will prevent repacking.

- [jakcron/nstool](https://github.com/jakcron/nstool)
- [Thealexbarney/LibHac](https://github.com/Thealexbarney/LibHac)
   Download `hactoolnet`
- hacpack
   The original `hacpack` repository has been deleted, and you must compile it from a fork repository. Linux users can try using the pre-compiled `hacpack` in this repository, Windows users need to compile it themselves.

```plain
Example directory structure:
.
├── hacpack
├── hactoolnet
├── main.py
└── nstool
```

### Extracting NSP Files

```bash
python main.py extract <path_to_nsp_file> [-o output_directory]
```

Options:

- `-o, --output`: Specify output directory, defaults to "out-nsp"

Example:

```bash
python main.py extract /path/to/game.nsp -o extracted_game
```

### Editing NSP Information

```bash
python main.py edit <directory_path> [-t TitleID] [-n Game_Name] [-a Author] [-v Version]
```

Options:

- `-t, --title_id`: New TitleID (e.g., 0100000000010000)
- `-n, --name`: Game name
- `-a, --author`: Game author
- `-v, --version`: Display version

Example:

```bash
python main.py edit extracted_game -t 0100000000010000 -n "My Game" -a "Me" -v "1.0.0"
```

### Packing NCA Files

```bash
python main.py pack <input_directory> -t <title_id> [-o output_directory] [-k key_file_path]
```

Options:

- `-t, --titleid`: TitleID (e.g., 0100000000010000)
- `-o, --output`: Specify output directory, defaults to "outNCA"
- `-k, --key`: Key file path, defaults to "key.dat"

Example:

```bash
python main.py pack extracted_game -t 0100000000010000 -o packaged_game
```

## Notes

- Please ensure you have legal rights to the game content before using this tool
- When editing NSP files, make sure the title_id is in the correct format (16 hexadecimal characters)
- You need to prepare a valid key file before packing

## License Notes

Third-party tools included or used in this repository are subject to their respective licenses:

- **nstool**: Please refer to the license of [jakcron/nstool](https://github.com/jakcron/nstool)
- **hactoolnet**: Please refer to the license of [Thealexbarney/LibHac](https://github.com/Thealexbarney/LibHac)
- **hacpack**: The original license applies. If you use the pre-compiled version in this repository, you do so at your own risk

If you redistribute these tools, please ensure compliance with their respective license terms.
