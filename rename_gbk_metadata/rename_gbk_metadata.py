#! /usr/bin/env python

"""
Renames some genbank metadata (LOCUS, DEFINITION, ACCESSION) that start with 
generic 'contig' or 'scaffold' strings and inserts the filename
It also updates the date
"""

from pathlib import Path
from argparse import ArgumentParser
from collections import defaultdict
from Bio import SeqIO
from datetime import date

__author__ = "Jorge Navarro"
__version__ = "1.0"
__maintainer__ = "Jorge Navarro"
__email__ = "jorge.navarromunoz@wur.nl"


def parameter_parser():
    parser = ArgumentParser(
        description="Renames generic genbank metadata beginning with 'contig' \
            or 'scaffold' inserting the filename in front"
    )

    parser.add_argument(
        "-i",
        "--inputfolder",
        help="Base folder with files. It will be searched recursively for \
            GenBank (.gb, .gbk, .gbff) files",
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
        help="Prints all filenames that were modified",
    )
    parser.add_argument(
        "--update_date",
        default=False,
        action="store_true",
        help="Updates date in GenBank headers to today"
    )

    return parser.parse_args()


def collect_files(input_folder):
    """
    Collects all files and makes sure filenames are unique
    """

    allowed_extensions = {"gb", "gbk", "gbff"}

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


def modify_metadata(
    gb_file: Path, base_output_folder: Path, verbose=False, update_date=False
) -> bool:
    """
    Opens and scans a genbank file, inserting the filename in front of the
    current value of the `locus` feature
    The modified data is written in a different output folder

    Returns:
    Output (bool): whether any header was fixed
    """

    filename = gb_file.stem
    header_fixed = False

    if base_output_folder is not None:
        output_folder = base_output_folder / Path("/".join(gb_file.parts[1:-1]))
        output_folder.mkdir(parents=True, exist_ok=True)
        output_file = output_folder / gb_file.name
    else:
        output_file = gb_file

    try:
        records = list(SeqIO.parse(gb_file, "genbank"))
    except ValueError as e:
        exit("Error: not able to parse file {gb_file}")
    else:
        for record in records:
            # record.id     modifies *both* ACCESSION and VERSION
            # record.name   modifies LOCUS
            if not record.id.startswith(filename):
                record.id = f"{filename}_{record.id}"
                header_fixed = True

            if not record.name.startswith(filename):
                record.name = f"{filename}_{record.name}"
                header_fixed = True

            today = date.today().strftime('%d-%b-%Y').upper()
            if update_date and record.annotations["date"] != today:
                # Month abbreviation *must* be capitalized
                record.annotations["date"] = today
                header_fixed = True

    with open(output_file, "w") as gb:
        SeqIO.write(records, gb, "genbank")
        if verbose and header_fixed:
            print(output_file)


def modify_in_place(gb_file: Path, verbose=False) -> bool:
    """
    Opens and scans a genbank file, inserting the filename to the header if
    it starts with 'contig'
    The original file is overwritten with the modified data

    Output (bool): whether any header was fixed
    """

    header_fixed = False

    modified_data = []
    with open(gb_file) as fasta:
        fasta_stem = gb_file.stem
        for line in fasta:
            if line[0] == ">":
                if line[1:].lstrip().lower().startswith("contig"):
                    header_fixed = True
                    modified_data.append(f">{fasta_stem}_{line[1:].lstrip()}")
                    continue

            modified_data.append(line)

    with open(gb_file, "w") as fasta:
        fasta.write("".join(modified_data))

    if verbose:
        print(gb_file)

    return header_fixed


def main():
    parameters = parameter_parser()

    # collect files
    file_list = collect_files(parameters.inputfolder)

    # modify files if necessary
    for fasta_file in sorted(file_list):
        modify_metadata(fasta_file, parameters.outputfolder, parameters.verbose,
                        parameters.update_date)


if __name__ == "__main__":
    main()
