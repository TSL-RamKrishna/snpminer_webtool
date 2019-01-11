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
parser.add_argument('--filter', action='store_true', dest='filter', default=False, help='Filter the SNPs')
parser.add_argument('--compare', action='store_true', dest='compare', default=False, help='Compare the SNPs')



options=parser.parse_args()
if not options.vcf:
	print("Input VCF file/s not provided. Use option --vcf to provde the input VCF files (mutliple vcf files should be space separated)")
	exit(1)
if len(options.vcf) ==1 and options.compare == True:
	print("Number of VCF files provided : ", len(options.vcf))
	print("SNP compare will not be done.")
	options.compare=False



vcffilenames  = options.vcf

snpsites={}		# declare a dict type to store chromosome and snp positions

for vcffilename in vcffilenames:
	fh=open(vcffilename, 'r')
	snpStart=False
	for line in fh:
		line=line.rstrip()
		if line.startswith("#CHROM"):
			snpStart=True
			continue
		elif line == "":
			continue
		else:

			if snpStart == True:
				print(line)
				linearray=line.split("\t")
				chromosome=linearray[0]
				position=linearray[1]
				ref=linearray[3]
				alt=linearray[4]
				if  chromosome in snpsites.keys():
					if position in snpsites[chromosome].keys():
						continue
					else:
						snpsites[chromosome][position] = [False] * len(vcffilenames)
				else:
					snpsites.update({chromosome:{str(position): [False] * len(vcffilenames) }})

	fh.close()



class filter_vcf_records():
	'''
	a class to filter the vcf records based on the thresholds provided
	'''

	def __init__(self, frequency=75, pvalue=0.05, genotype='heterozygous', genotype_quality=30, raw_read_depth=10, quality_read_depth=10, depth_in_reference=10, depth_in_variant=10):
		''' Initialize the filter parameters with default values, if not provided'''

		self.frequency=frequency
		self.pvalue=pvalue
		self.genotype=genotype
		self.genotype_quality=genotype_quality
		self.raw_read_depth=raw_read_depth
		self.quality_read_depth=quality_read_depth
		self.depth_in_reference=depth_in_reference
		self.depth_in_variant=depth_in_variant
	def set_filename(self, vcf):
		self.vcf=vcf
	def get_record(self, record):
		self.record=record
		self.samplename = self.record.samples[0]
	def filter_records(self):
		''' Calls the filter class - get_passed_filter_records function to get the snp records that pass the filter step'''
		filter = filter.get_passed_filter_records(self.vcf, self.frequency, self.pvalue, self.genotype, self.genotype_quality, self.raw_read_depth, self.quality_read_depth, self.depth_in_reference, self.depth_in_variant)
	def filter_a_record(self):
		''' filter one record at a time '''
		return passed_filter(self.record, self.samplename)


class compare_vcf_records():
	def __init__(self,database):
		self.database=database
		self.comparing=compareSNPs(self.database)
	def get_common_records(self):
		self.common_records=self.comparing.get_common_records()
		# you may write common records to file
	def get_unique_records(self):
		self.uniq_record_db = self.comparing.get_unique_records()
	def write_unique_records_snps(self):
		for key in self.uniq_record_db.keys():
			print("Key: ", key)
			filename=self.uniq_record_db[key]["filename"]
			vcf_reader=vcf.Reader(open(filename, 'r'))
			vcf_writer=vcf.Writer(open(filename + "uniqueRecords.vcf", 'w'), vcf_reader)
			for record in self.uniq_record_db[key]['uniqueRecords']:
				#print("Uniq records: ", len(self.uniq_record_db[key]['uniqueRecords']))
				vcf_writer.write_record(record)
	def write_common_records_snps(self):
		out=open('testfiles/common_records.txt', 'w')
		for record in self.common_records:
			out.write(" ".join(map(str,[record.CHROM, record.POS, record.REF, record.ALT, "\n"]) ) )

def read_vcf_records(vcf_filename):
	return list(vcf.Reader(filename=vcf_filename))

#construct a database of vcf filename and records

vcf_database={}
counter=1
for vcfinput in options.vcf:
	vcf_database["inputfile-" + str(counter)]={'filename':vcfinput, 'snp_positions':{}}
	counter+=1


# Read the snps from vcf and filter them one by one.

if options.filter == True:
	inputvcf = filter_vcf_records()  # create object to filter records

	for key in vcf_database.keys():
		vcf_reader=vcf.Reader(open(vcf_database[key]['filename']), 'r')
		for record in vcf_reader:
			chromosome, position, ref, alt = record.CHROM, record.POS, record.REF, record.ALT
			inputvcf.get_record(record)
			filter_result = inputvcf.filter_a_record()
			if filter_result == True:
				if  vcf_database[key]['snp_positions'].keys():





if options.compare == True:
	compare = compare_vcf_records(vcf_database)
	compare.get_common_records()
	compare.get_unique_records()
	compare.write_common_records_snps()
	compare.write_unique_records_snps()
	## To compare the SNPs, we need at least two vcf files
	## for vcf files x, y and z, compare snps will output x - y, x - z
