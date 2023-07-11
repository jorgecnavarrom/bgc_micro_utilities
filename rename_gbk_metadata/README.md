# Rename fasta headers

This small script attempts to modify some metadata in the header of GenBank files. It will add the filename in front of the `LOCUS` feature. Additionally, it can update the date

The script will throw an error if it detects non-unique filenames (regardless of location within the folder substructure)

## Help

```
$ python rename_gbk_metadata.py -h
usage: rename_gbk_metadata.py [-h] -i INPUTFOLDER [-o OUTPUTFOLDER] [--verbose] [--update_date]

Renames generic genbank metadata beginning with 'contig' or 'scaffold' inserting the filename in front

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFOLDER, --inputfolder INPUTFOLDER
                        Base folder with files. It will be searched recursively for GenBank (.gb, .gbk, .gbff) files
  -o OUTPUTFOLDER, --outputfolder OUTPUTFOLDER
                        Base output directory. If given, it will create a copy instead of modifying the files in-place. It will re-create the folder structure within the input folder
                        (Note: this will replace results if the folder already exists)
  --verbose             Prints all filenames that were modified
  --update_date         Updates date in GenBank headers to today
```

## Examples

A successful run:

```
$ python rename_gbk_metadata.py -i gbk_test/ -o gbk_test_out --verbose
/home/jorge/miniconda3/envs/bgclib/lib/python3.8/site-packages/Bio/SeqIO/InsdcIO.py:726: BiopythonWarning: Increasing length of locus line to allow long name. This will result in fields that are not in usual positions.
  warnings.warn(
gbk_test_out/Mycreb1.region001.gbff
gbk_test_out/Mycreb1.region002.gbk
gbk_test_out/Mycreb1.region005.gbk
gbk_test_out/Mycreb1.region006.gbk
gbk_test_out/subfolder/Mycreb1_.region005.gb
gbk_test_out/subfolder/x/Mycreb1.region003.gbk
gbk_test_out/subfolder/x/Mycreb1.region004.gb
```

(note: the Biopython warning won't affect the tool)

Problems with filename uniqueness:

```
$ python rename_gbk_metadata.py -i gbk_test/ -o gbk_test_out --verbose
Error: Some filenames are not unique!
Mycreb1.region005:
        gbk_test/subfolder/Mycreb1.region005.gb
        gbk_test/Mycreb1.region005.gbk
```

## Requirements

* Python 3
* Biopython (v1.77 tested)
