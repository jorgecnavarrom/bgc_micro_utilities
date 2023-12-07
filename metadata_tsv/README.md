# Metadata TSV

This script helps creating tsv files for metadata annotation of gbk files (useful as imported annotations in e.g. Cytoscape).

The first column contains the name (without extension) of gbk files found in the input folder, and the second column contains a user-defined annotation

## Help

```
$ python metadata_tsv.py -h
usage: metadata_tsv.py [-h] -i INPUT_FOLDER [-t TSV_NAME] -a ANNOTATION -v VALUE [--include [INCLUDE ...]]

Helps creating a metadata tsv file. First column is the name (without extention) of a gbk file; Second column is a user-defined annotation

options:
  -h, --help            show this help message and exit
  -i INPUT_FOLDER, --input_folder INPUT_FOLDER
                        Folder with region.gbk files
  -t TSV_NAME, --tsv_name TSV_NAME
                        Path to the output tsv file. Intermediate folders will be created if necessary
  -a ANNOTATION, --annotation ANNOTATION
                        The title of the annotation (e.g. Reference set)
  -v VALUE, --value VALUE
                        The value of the annotation to use in the second column (e.g. MIBiG, Literature)
  --include [INCLUDE ...]
                        A list of strings that can be present in the file name in order to be included. If missing, every .gbk file will be included. Default: 'region'
```

## Examples

The following command:

```bash
python metadata_tsv.py --input_folder ~/databases/MIBiG/3.1 --tsv_name annotations_reference.tsv --annotation Reference Set --value 'MIBiG 3.1' --include BGC
```

Will create a file `annotations_reference.tsv` which looks like:

```
Region  Reference Set
BGC0000972      MIBiG 3.1
BGC0000966      MIBiG 3.1
BGC0002181      MIBiG 3.1
BGC0001488      MIBiG 3.1
BGC0000796      MIBiG 3.1
BGC0000782      MIBiG 3.1
BGC0002195      MIBiG 3.1
...
```

## Requirements

* Python 3
