#!/usr/bin/env python3

"""
Finds gbk files and labels them in a tsv file

Example:
python tsv_annotate.py -i ./inputdata/lichen -t annotation_niche_lichen.tsv
    -a Niche -v Lichen

will produce a file called 'annotation_niche_lichen.tsv' that looks like:
Region	Niche
genomeregion1
"""

from pathlib import Path
import argparse


def parameter_parser():
    parser = argparse.ArgumentParser(
        description="Helps creating a metadata tsv file. First column is the \
            name (without extention) of a gbk file; Second column is a \
            user-defined annotation"
    )

    parser.add_argument(
        "-i",
        "--input_folder",
        help="Folder with region.gbk files",
        required=True,
        type=Path
    )

    parser.add_argument(
        "-t",
        "--tsv_name",
        help="Path to the output tsv file. Intermediate folders will be created\
            if necessary",
        type=Path,
        default=Path("./region_annotations.tsv")
    )

    parser.add_argument(
        "-a",
        "--annotation",
        help="The title of the annotation (e.g. Reference set)",
        required=True
    )

    parser.add_argument(
        "-v",
        "--value",
        help="The value of the annotation to use in the second column (e.g. \
            MIBiG, Literature)",
        required=True
    )

    parser.add_argument(
        "--include",
        help="A list of strings that can be present in the file name in order \
            to be included. If missing, every .gbk file will be included. \
            Default: 'region'",
        default=["region"],
        nargs="*"
    )

    return parser.parse_args()


def make_tsv(parameters):
    """Collects gbk files from input folder and annotates them in a tsv file
    """

    # collect parameters
    input_folder = parameters.input_folder
    if not input_folder.is_dir():
        exit("Error: invalide input folder")

    tsv_path = parameters.tsv_name
    if tsv_path.name == "":
        exit("Error: empty tsv name")

    annotation = parameters.annotation
    value = parameters.value

    include_list = parameters.include
 
    # Scan input folder for gbk files
    gbk_list = list(input_folder.glob("**/*.gbk"))
    if len(gbk_list) == 0:
        print("No gbk files were found in the input folder")
        exit()

    # validate list with allowed substrings
    gbk_validated = []
    for gbk in gbk_list:
        if len(include_list) == 0:
            gbk_validated.append(gbk)
        else:
            for include_string in include_list:
                if include_string in gbk.name:
                    gbk_validated.append(gbk)
                    break

    print(f"Found {len(gbk_validated)} gbk files")

    output_folder = Path(tsv_path.parent)
    output_folder.mkdir(parents=True, exist_ok=True)
    with open(tsv_path, "w") as tsv:
        tsv.write(f"Region\t{annotation}\n")
        for gbk in gbk_validated:
            tsv.write(f"{gbk.stem}\t{value}\n")


def main():
    parameters = parameter_parser()
    make_tsv(parameters)


if __name__ == "__main__":
    main()