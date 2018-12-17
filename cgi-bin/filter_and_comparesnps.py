#!/usr/bin/env python3
import os, sys, re
import numpy as np
import argparse
import vcf

rootPath=os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(rootPath)

from vcfFilter import filter
from compare_snps import compareSNPs

parser=argparse.ArgumentParser(description='Script to filter the SNPs using user threshold values and compare the SNPs from multiple VCF files')

parser.add_argument('--vcf', action='store', dest='vcf', nargs='+', help='Space separated vcf input files')
parser.add_argument('--filter', action='store_true', dest='filter', help='Filter the SNPs')
parser.add_argument('--compare', action='store_true', dest='compare', help='Compare the SNPs')



options=parser.parse_args()

print (options)



class filter_vcf_records():

	def __init__(self, vcf, frequency=75, pvalue=0.05, genotype='heterozygous', genotype_quality=30, raw_read_depth=10, quality_read_depth=10, depth_in_reference=10, depth_in_variant=10):
		self.vcf=vcf
		self.frequency=frequency
		self.pvalue=pvalue
		self.genotype=genotype
		self.genotype_quality=genotype_quality
		self.raw_read_depth=raw_read_depth
		self.quality_read_depth=quality_read_depth
		self.depth_in_reference=depth_in_reference
		self.depth_in_variant=depth_in_variant
	def filter_records(self):
		filter = filter.get_passed_filter_records(self.vcf, self.frequency, self.pvalue, self.genotype, self.genotype_quality, self.raw_read_depth, self.quality_read_depth, self.depth_in_reference, self.depth_in_variant)


class compare_vcf_records():
	def __init__(self,database):
		self.database=database
		self.comparing=compareSNPs(self.database)
	def get_common_records(self):
		self.common_records=self.comparing.get_common_records()
		# you may write common records to file
	def get_unique_records(self):
		self.record_db = self.comparing.get_unique_records()
	def write_unique_records(self):
		for key in self.record_db.keys():
			filename=self.record_db[key]["filename"]
			vcf_reader=vcf.Reader(open(filename, 'r'))
			vcf_writer=vcf.Writer(open(filename + "uniqueRecords.vcf", 'w'), vcf_reader)
			for record in self.record_db[key]['uniqueRecords']:
				vcf_writer.write_record(record)
	def write_common_records(self):
		vcf_reader=vcf.Reader(open(self.database[0]['filename'], 'r'))
		vcf_writer=vcf.Writer(open('testfiles/commonrecords.vcf', 'w'), vcf_reader)
		for record in self.common_records:
			vcf_writer.write_record(record)


vcf_database={}
counter=1
for vcf in options.vcf:
	print (vcf)
	if options.filter == True:
		filter_passed_records=filter(vcf)
		vcf_database["inputfile-" + str(counter)]={'filename':vcf, 'filterPassedRecord':filter_passed_records.get_passed_filter_records(), 'uniqueRecords':[], 'commonrecords':[]}
		filter_passed_records.write_vcf('testfiles/filter_test_output.vcf', vcf_database["inputfile-" + str(counter)]['filterPassedRecord'])
		counter+=1

for key in vcf_database:
	print key, len(vcf_database[key]['filterPassedRecord'])


compare = compare_vcf_records(vcf_database)
compare.get_common_records()
compare.get_unique_records()
compare.write_common_records()
compare.write_unique_records()
## To compare the SNPs, we need at least two vcf files
## for vcf files x, y and z, compare snps will output x - y, x - z
