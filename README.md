# GenFetcher
Python tool to download data from NCBI


### Download modules

A download module is included in the program. This allows the user to quickly download genomic data from NCBI.

| Options                       | Type          | Output                                                                | Default |
| ----------------------------- |:-------------:|:--------------------------------------------------------------------- |:-------:|
| -d, --download                | Boolean       | Download genome data from NCBI.                                       | False   |


## Download Module

```
python genfetcher.py -d
```
This option will start the download module that is used to fetch data directly from NCBI, the genome data is obtained with the accession numbers. The usage of this module is listed below:

* First, it will ask for an email to send to the NCBI servers for authentication
* The program will ask if the user wants to manually input the accession [Y] numbers or pass a file with them [n].
  * The accession numbers must be separated by a comma.
  * The file with the accession numbers must be in a list fashion way.
* Next, the user must input a directory to save the data (if this directory not exists, it will be created)
* Finally it will be asked if the user want's to download the FASTA files or Genbank files.

If by any reason the download is halted, the program will check if any of the files to be downloaded are already in the specified directory and skip them.
