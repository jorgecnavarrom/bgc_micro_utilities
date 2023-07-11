# Rename fasta headers

This small script attempts to modify all fasta headers that begin with the string `contig` by inserting the filename (without the extension).

The script will throw an error if it detects non-unique filenames (regardless of location within the folder substructure)

## Help

```
$ python rename_fasta_headers.py -h
usage: rename_fasta_headers.py [-h] -i INPUTFOLDER [-o OUTPUTFOLDER] [--verbose]

Renames all fasta headers beginning with 'contig' by inserting the filename in front

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFOLDER, --inputfolder INPUTFOLDER
                        Base folder with files. It will be searched recursively for .fasta files
  -o OUTPUTFOLDER, --outputfolder OUTPUTFOLDER
                        Base output directory. If given, it will create a copy instead of modifying the files in-place. It will re-create the folder structure within the input folder
                        (Note: this will replace results if the folder already exists)
  --verbose             Prints all filenames that were fixed
```

## Examples

A successful run:

```bash
python rename_fasta_headers.py -i input_test/ -o fasta_out --verbose
fasta_out/CP016438.fasta
fasta_out/CP007699.fasta
fasta_out/subfolder/1/an example.fasta
fasta_out/subfolder/1/excellent.fasta
fasta_out/subfolder/1/2/AL645882.fasta
```

Problems with filename uniqueness:

```bash
$ python rename_fasta_headers.py -i input_test/ -o fasta_out --verbose
Error: Some filenames are not unique!
CP007699:
        input_test/CP007699.fasta
        input_test/subfolder/1/CP007699.fasta
```

## Requirements

* Python 3
