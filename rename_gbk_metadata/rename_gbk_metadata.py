#! /usr/bin/env python

"""
Renames some genbank metadata (LOCUS, DEFINITION, ACCESSION) that start with 
generic 'contig' or 'scaffold' strings and inserts the filename.
Optionally, the string can be replaced entirely with some other string (see
option --external).
It also updates the date.
"""

from pathlib import Path
from argparse import ArgumentParser
from collections import defaultdict
from Bio import SeqIO
from datetime import date

__author__ = "Jorge Navarro"
__version__ = "1.1"
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

    parser.add_argument(
        "-e",
        "--external",
        help="Provide an external dictionary for the string substitution. \
            It should be a tab-separated file with two columns: the first being\
            the base filename (from e.g. [BASE FILENAME].region001.gbk) and the\
            second, the string to use for replacement in the metadata.",
        type=Path
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


def parse_dict_file(external_dict_file:Path) -> dict:
    """
    Reads and parses a two column tsv file with
    Col1 = base filename in the input folders
    Col2 = string to use in metadata (e.g. a short label, strain etc)
    """

    original_to_substitute = {}
    with open(external_dict_file) as edf:
        for line in edf:
            if line[0] == "#":
                continue
            try:
                original, substitute = line.strip().split("\t")
            except ValueError:
                exit(f"Something went wrong while trying to read line\n{line}")
            else:
                original_to_substitute[original] = substitute

    if len(original_to_substitute) == 0:
        exit("Error: no data found in the external dictionary file")

    print(f"Found an external dictionary file with {len(original_to_substitute)} substitutions")

    return original_to_substitute


def modify_metadata(
    gb_file: Path, base_output_folder: Path, substitute_strings: dict, 
    verbose=False, update_date=False,
) -> bool:
    """
    Opens and scans a genbank file, inserting the filename in front of the
    current value of the `locus` feature
    The modified data is written in a different output folder

    Returns:
    Output (bool): whether any header was fixed
    """

    filename = gb_file.stem
    prefix = filename.split(".region")[0]
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

            # Attempt to forcibly replace string if external dictionary provided
            if substitute_strings and prefix in substitute_strings:
                record.id = f"{substitute_strings[prefix]}"
                record.name = f"{substitute_strings[prefix]}"
                header_fixed = True

            # else, simply append filename at the beginning
            else:
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


def main():
    parameters = parameter_parser()

    # collect files
    file_list = collect_files(parameters.inputfolder)

    # optionally, look for an external dictionary file
    substitute_strings = {}
    if parameters.external:
        substitute_strings = parse_dict_file(parameters.external)

    # modify files if necessary
    for gb_file in sorted(file_list):
        modify_metadata(gb_file, parameters.outputfolder, substitute_strings, 
                        parameters.verbose, parameters.update_date)


if __name__ == "__main__":
    main()
