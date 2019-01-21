#!/usr/bin/env python3
import os, sys, re
import numpy as np
import argparse
import vcf

rootPath=os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(rootPath)

from vcfFilter import filter

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
snp_positions={}


class filter_vcf_records():
	'''
	a class to filter the vcf records based on the thresholds provided
	'''

	def __init__(self, frequency=75, pvalue=0.05, genotype='heterozygous', genotype_quality=10, raw_read_depth=1, quality_read_depth=1, depth_in_reference=1, depth_in_variant=1):
		''' Initialize the filter parameters with default values, if not provided'''
		self.filter=filter(frequency, pvalue, genotype, genotype_quality, raw_read_depth, quality_read_depth, depth_in_reference, depth_in_variant)
	def set_filename(self, vcf):
		self.vcf=vcf
	def set_record(self, record, samplename):
		self.record=record
		self.samplename = samplename

	def filter_records(self):
		''' Calls the filter class - get_passed_filter_records function to get the snp records that pass the filter step'''
		filter = self.filter.get_passed_filter_records(self.vcf, self.frequency, self.pvalue, self.genotype, self.genotype_quality, self.raw_read_depth, self.quality_read_depth, self.depth_in_reference, self.depth_in_variant)
	def filter_a_record(self):
		''' filter one record at a time '''
		return self.filter.passed_filter(self.record, self.samplename)



def create_db_for_all_snps(chromosome, position ):

	if  chromosome in snpsites.keys():
		if position in snpsites[chromosome].keys():
			return
		else:
			snpsites[chromosome][str(position)] = [False] * len(vcffilenames)
	else:
		snpsites.update({chromosome:{str(position): [False] * len(vcffilenames) }})


def filter_snps(do_filter=False):


	for key_counter in range(len(vcffilenames)):
		vcf_reader=vcf.Reader(open(vcffilenames[key_counter]), 'r')
		samplename= vcf_reader.samples[0]
		for record in vcf_reader:
			chromosome, position, ref, alt = record.CHROM, record.POS, record.REF, record.ALT
			position=str(position)

			## code to build all snps position
			create_db_for_all_snps(chromosome, position)

			inputvcf.set_record(record, samplename)
			filter_result = inputvcf.filter_a_record()
			if do_filter==True:
				if filter_result == True:

					snp_positions.update({str(key_counter) + "_" + chromosome + "_" + str(position):{'ref': str(ref), 'alt':str(alt).replace("[","").replace("]", "")}})
					snpsites[chromosome][str(position)][key_counter]= True

			else:
				snp_positions.update({str(key_counter) + "_" + chromosome + "_" + str(position):{'ref': str(ref), 'alt':str(alt).replace("[","").replace("]", "")}})
				snpsites[chromosome][str(position)][key_counter]= True


def get_unique_snps():
	''' Get snps unique to a vcf file '''

	for key_counter in range(len(vcffilenames)):
		for chromosome in snpsites.keys():
			for position in snpsites[chromosome].keys():
				snp_array_in_bool = iter(snpsites[chromosome][position])
				if snpsites[chromosome][position][key_counter] == True and sum(snpsites[chromosome][position]) == 1:  # First any(array) finds first True and second any(array) finds another True, if second True, it will say False
					# This is unique snp
					#vcf_database[key]['unique_snps'].append([chromosome, position, vcf_database[key]['snp_positions'][chromosome + "_" + position]['ref'], ",".join(vcf_database[key]['snp_positions'][chromosome + "_" + position]['alt']) ])
					snp_positions[str(key_counter) + "_" + chromosome + "_" + position].update({'unique':True})
				#else:
				#	vcf_database['snp_positions'][chromosome + "_" + position].update({'unique':False})
	return

def get_common_snps():

	''' Get snps common to all vcf files'''
	for key_counter in range(len(vcffilenames)):
		for chromosome in snpsites.keys():
			for position in snpsites[chromosome].keys():
				if all(snpsites[chromosome][position]) == True:
					snp_positions[str(key_counter) + "_" + chromosome + "_" + position].update({'common' : True})
				#else:
				#	vcf_database[key]['snp_positions'][chromosome + "_" + positon].update({'common' : True})


def get_snp_data():
	print
	for key_counter in range(len(vcffilenames)):
		print("Filename: ", vcffilenames[key_counter])
		for snp in snp_positions.keys():
			if snp.startswith(str(key_counter)):

				if 'common' in snp_positions[snp].keys():
					print(" ".join(snp.replace("_" ," ").split(" ")[1:]), snp_positions[snp]['ref'], snp_positions[snp]['alt'].replace(" ", ""), 'common')
				elif 'unique' in snp_positions[snp].keys():
					print(" ".join(snp.replace("_" ," ").split(" ")[1:]), snp_positions[snp]['ref'],  snp_positions[snp]['alt'].replace(" ", ""), 'unique')

		print("\n")

	return

def save_command_unique_snps():

	for key_counter in range(len(vcffilenames)):
		outfh=open(vcffilenames[key_counter] + "_snpanalysis.txt", "w")
		for snp in snp_positions.keys():
			if snp.startswith(str(key_counter)):
				if 'common' in snp_positions[snp].keys():
					outfh.write(" ".join(snp.replace("_" ," ").split(" ")[1:]) + snp_positions[snp]['ref'] + snp_positions[snp]['alt'].replace(" ", "") + 'common' + "\n" )
				elif 'unique' in snp_positions[snp].keys():
					outfh.write(" ".join(snp.replace("_" ," ").split(" ")[1:]) + snp_positions[snp]['ref'] + snp_positions[snp]['alt'].replace(" ", "") + 'unique' + "\n")

		outfh.close()

	return

def compare_snps():

	get_unique_snps()
	get_common_snps()


#construct a database of vcf filename and records




# Read the snps from vcf and filter them one by one.

inputvcf = filter_vcf_records()  # create object to filter records
if options.filter == True:
	filter_snps(True)
else:
	filter_snps(False)

if options.compare == True:
	get_unique_snps()
	get_common_snps()
	#compare = compare_vcf_records(vcf_database)
	#compare.get_common_records()
	#compare.get_unique_records()
	#compare.write_common_records_snps()
	#compare.write_unique_records_snps()
	## To compare the SNPs, we need at least two vcf files
	## for vcf files x, y and z, compare snps will output x - y, x - z

get_snp_data()
save_command_unique_snps()

exit(0)
