## 15 June 2018

Add the code that detects multiple samples in a VCF file and alerts user about this. Gives user a choice to split the VCF file by sample.

## 18 June 2018

A bug found. While uploading multiple files, only the first file is validated, other files are not checked. The bug is fixed

Another bug found. While uploading new files by clicking add button, these new files are not validated. The bug is fixed.


## 25 June 2018

Get the sample names from multisample VCF file. Display the samples from multisample vcf file. Ask user the name of sample to split out

## July 2018

User uploading multiple sample vcf can now tick to choose one or more samples and has an option to combine selected samples.

## Aug and september 2018

Working on multiple file upload to web server. Single file upload was successful, however, multiple file upload has not been successful so far.

## 17 September

Tested multiple file upload using separate html page successfully

## 24 September

Error found when one sample is selected from multiple sample vcf file. The file is created for each letter in the sample name. This is fixed now.

Another error found was, when multiple samples are selected from multisample vcf, the merging and indexing was not happening. This is fixed now

## 08 December

Unit testing for the script vcfFilter.py completed. 22 tests in total

## 17 December

Rewriting the whole package. The script filter_and_comparesnps.py is the master script that calls filter functions and compare functions. It's nearly done.
