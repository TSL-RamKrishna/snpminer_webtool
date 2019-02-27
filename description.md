## Description

snpFC is a Bioinformatic tool for filtering and comparing Single Nucleotide Polymorphisms (SNPs) from two or more input VCF files.

SNPs are filtering if they user specified threshold parameter values are not satisfied. Filtered out SNPs are removed and not considered in the SNS comparison step. See help for filter parameters. Default threshold values are used for filtering if not specified.

SNPs are compared to check if it is a unique to a sample or common to all samples. The output shows 5 column data - chromosome, position, RefBase, AltBase and common or unique keyword.
