#!/usr/bin/env python3
import sys
import argparse

from src.edit import edit_nacp_file, edit_npdm_title_id
from src.extract import process_nsp_file
from src.pack import pack_nca_files, pack_nsp


def main():
    # Create main parser
    parser = argparse.ArgumentParser(description="NSP File Processing Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create extract subcommand parser
    extract_parser = subparsers.add_parser("extract", help="Parse and extract NSP files")
    extract_parser.add_argument("nsp_path", help="Path to NSP file")
    extract_parser.add_argument("-o", "--output", default="out-nsp", help="Output directory")

    # Create edit subcommand parser
    edit_parser = subparsers.add_parser("edit", help="Edit NSP files")
    edit_parser.add_argument("directory", help="Path to directory containing program and control files")
    edit_parser.add_argument(
        "-t", "--title_id", help="New titleId, in 16-character hexadecimal format"
    )
    edit_parser.add_argument("-n", "--name", help="Game name")
    edit_parser.add_argument("-a", "--author", help="Game author")
    edit_parser.add_argument("-v", "--version", help="Display version")

    # Create pack subcommand parser
    pack_parser = subparsers.add_parser("pack", help="Pack NCA files")
    pack_parser.add_argument(
        "input_dir", help="Input directory (containing extracted control and program directories)"
    )
    pack_parser.add_argument(
        "-t", "--titleid", required=True, help="Title ID (e.g.: 0100000000010000)"
    )
    pack_parser.add_argument("-o", "--output", default="outNCA", help="Output directory")
    pack_parser.add_argument("-k", "--key", default="key.dat", help="Path to key file")

    args = parser.parse_args()

    # Call corresponding functions based on subcommand
    if args.command == "extract":
        process_nsp_file(args.nsp_path, args.output)
    elif args.command == "pack":
        pack_nca_files(args.input_dir, args.titleid, args.output, args.key)
        pack_nsp(args.output, args.titleid, args.key)
    elif args.command == "edit":
        edit_npdm_title_id(args.directory, args.title_id)
        edit_nacp_file(
            args.directory, args.title_id, args.name, args.author, args.version
        )
    elif not args.command:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
