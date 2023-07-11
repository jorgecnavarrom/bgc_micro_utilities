#! /usr/bin/env python

"""
Renames fasta headers that start with 'contig', adding the filename in front
"""

from pathlib import Path
from argparse import ArgumentParser
from collections import defaultdict

__author__ = "Jorge Navarro"
__version__ = "1.0"
__maintainer__ = "Jorge Navarro"
__email__ = "jorge.navarromunoz@wur.nl"


def parameter_parser():
    parser = ArgumentParser(
        description="Renames all fasta headers beginning with 'contig' by \
            inserting the filename in front"
    )

    parser.add_argument(
        "-i",
        "--inputfolder",
        help="Base folder with files. It will be searched recursively for \
            .fasta files",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "-o",
        "--outputfolder",
        help="Base output directory. If given, it will create a copy \
            instead of modifying the files in-place. It will re-create the \
            folder structure within the input folder (Note: this will \
            replace results if the folder already exists)",
        type=Path,
    )
    parser.add_argument(
        "--verbose",
        default=False,
        action="store_true",
        help="Prints all filenames that were fixed",
    )

    return parser.parse_args()


def collect_files(input_folder: Path) -> list:
    """
    Collects all files and makes sure filenames are unique
    """

    allowed_extensions = {"fasta"}

    filename_count = defaultdict(list)
    paths_files = []
    for extension in allowed_extensions:
        paths_files.extend(input_folder.glob(f"**/*.{extension}"))

    # keep a counter of how many file paths match a given filename
    for file_path in paths_files:
        filename = file_path.stem
        filename_count[filename].append(file_path)

    # stop if filenames are not unique (notice extension could be different)
    max_filename_count = max([len(x) for x in filename_count.values()])
    if max_filename_count > 1:
        print("Error: Some filenames are not unique!")
        for filename, file_paths in filename_count.items():
            if len(file_paths) > 1:
                print(f"{filename}:")
                for file_path in file_paths:
                    print(f"\t{file_path}")
        exit()

    return paths_files


def create_fixed_fasta(
    fasta_file: Path, base_output_folder: Path, verbose=False
) -> bool:
    """
    Opens and scans a fasta file, inserting the filename to the header if
    it starts with 'contig'
    The modified data is written in a different output folder

    Output (bool): whether any header was fixed
    """

    header_fixed = False
    output_folder = base_output_folder / Path("/".join(fasta_file.parts[1:-1]))
    output_folder.mkdir(parents=True, exist_ok=True)
    with open(fasta_file) as fasta, open(output_folder / fasta_file.name, "w") as out:
        fasta_stem = fasta_file.stem
        for line in fasta:
            if line[0] == ">":
                if line[1:].lstrip().lower().startswith("contig"):
                    header_fixed = True
                    out.write(f">{fasta_stem}_{line[1:].lstrip()}")
                    continue

            out.write(line)

    if verbose:
        print(output_folder / fasta_file.name)

    return header_fixed


def modify_in_place(fasta_file: Path, verbose=False) -> bool:
    """
    Opens and scans a fasta file, inserting the filename to the header if
    it starts with 'contig'
    The original file is overwritten with the modified data

    Output (bool): whether any header was fixed
    """

    header_fixed = False

    modified_data = []
    with open(fasta_file) as fasta:
        fasta_stem = fasta_file.stem
        for line in fasta:
            if line[0] == ">":
                if line[1:].lstrip().lower().startswith("contig"):
                    header_fixed = True
                    modified_data.append(f">{fasta_stem}_{line[1:].lstrip()}")
                    continue

            modified_data.append(line)

    with open(fasta_file, "w") as fasta:
        fasta.write("".join(modified_data))

    if verbose:
        print(fasta_file)

    return header_fixed


def main():
    parameters = parameter_parser()

    # collect files
    file_list = collect_files(parameters.inputfolder)

    # create files if output folder specified
    if parameters.outputfolder:
        # create folder if necessary
        for fasta_file in file_list:
            create_fixed_fasta(fasta_file, parameters.outputfolder, parameters.verbose)

    # otherwise, modify existing files
    else:
        for fasta_file in file_list:
            modify_in_place(fasta_file, parameters.verbose)


if __name__ == "__main__":
    main()
