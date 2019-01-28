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
parser.add_argument('--frequency', action='store', dest='frequency', default=70, type=int, help='Frequency of SNP call. Default: 70 [int]')
parser.add_argument('--pvalue', action='store', dest='pvalue', default=0.05, type=float, help='Pvalue of the SNP call. Default: 0.05 [float]' )
parser.add_argument('--genotype', action='store', dest='genotype', default='heterozygous', type=str, help='Genotype of the SNP call - heterozygous/homozygous/both. Default: heterozygous')
parser.add_argument('--quality', action='store', dest='genotype_quality', default=10, type=int, help='Genotype quality of the SNP call. Default: 10')
parser.add_argument('--rawreaddepth', action='store', dest='raw_read_depth', default=5, type=int, help='Raw read depth of the SNP call. Default: 5')
parser.add_argument('--qualityreaddepth', action='store', dest='quality_read_depth', default=5, type=int, help='Quality read depth of the SNP call. Default: 5')
parser.add_argument('--depthreference', action='store', dest='depth_in_reference', default=5, type=int, help='Depth in reference of the SNP call. Default: 5')
parser.add_argument('--depthvariant', action='store', dest='depth_in_variant', default=5, type=int, help='Depth in variant of the SNP call. Default: 5')
parser.add_argument('--show', action='store_true', dest='display', default=False, help='Display the results on the screen')
parser.add_argument('--show', action='store_true', dest='display', default=False, help='Display the results on the screen')
parser.add_argument('--outdir', action='store', dest="outdir", default=os.path.abspath('.'), help='Path to the output folder. Default: Current working directory')



snpsites={}		# declare a dict type to store chromosome and snp positions from all vcfs
snp_positions={}	# stores chromosome, position, ref and alt for each vcf file
inputvcf = filter_vcf_records()	# instance of filtering

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

def add_snp_to_database(filename, chromosome, position, ref, alt):
	'append the snp records to the dictionary data structure once they passed the filter'

	if filename in snp_positions.keys():
		if chromosome in snp_positions[filename].keys():
			snp_positions[filename][chromosome].update({str(position):{'ref':ref, 'alt':str(alt).replace("[","").replace("]", "")}} )
		else:
			snp_positions[filename].update({chromosome:{str(position):{'ref':ref, 'alt':str(alt).replace("[","").replace("]", "")}}})
	else:
		snp_positions.update({filename:{chromosome:{str(position) : {'ref': ref, 'alt':str(alt).replace("[","").replace("]", "")}}}})


def filter_snps(do_filter=False):
	'Filter the snps using threshold values as defined'

	key_counter = 0
	for filename in  vcffilenames:
		vcf_reader=vcf.Reader(open(filename), 'r')
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
					add_snp_to_database(filename, chromosome, position, ref, alt)
					#snp_positions.update({str(key_counter) + "_" + chromosome + "_" + str(position):{'ref': str(ref), 'alt':str(alt).replace("[","").replace("]", "")}})
					snpsites[chromosome][str(position)][key_counter] = True
				else:
					pass

			else:
				add_snp_to_database(filename, chromosome, position, ref, alt)
				#snp_positions.update({str(key_counter) + "_" + chromosome + "_" + str(position):{'ref': str(ref), 'alt':str(alt).replace("[","").replace("]", "")}})
				snpsites[chromosome][str(position)][key_counter]= True

		key_counter+=1

def count_list_elements_occurrences(array):
	'return an array showing the count of each element of input array'
	counts=[]
	for x in array:
		counts.append(array.count(x))
	return counts


def get_unique_snps():
	''' Get snps unique to a vcf file '''

	key_counter = 0

	for chromosome in snpsites.keys():
		for position in snpsites[chromosome].keys():
			if snpsites[chromosome][position][key_counter] == True and sum(snpsites[chromosome][position]) == 1:  # First any(array) finds first True and second any(array) finds another True, if second True, it will say False
				# This is unique snp

				#vcf_database[key]['unique_snps'].append([chromosome, position, vcf_database[key]['snp_positions'][chromosome + "_" + position]['ref'], ",".join(vcf_database[key]['snp_positions'][chromosome + "_" + position]['alt']) ])
				snp_positions[vcffilenames[key_counter]][chromosome][position].update({'unique':True})
			elif sum(snpsites[chromosome][position]) >=2:		# there might be snp at same position but with different alt base

				snp_index = [i for i, j in enumerate(snpsites[chromosome][position]) if j==True]

				totalindex = len(snp_index)
				# Lets check the alt base in these vcf files using index
				# lets get array of alt bases from each file
				alt_snps=[]
				for index in snp_index:
					alt_snps.append(snp_positions[vcffilenames[index]][chromosome][position]['alt'])

				# get the counts of the elements

				counts = count_list_elements_occurrences(alt_snps)

				for index in range(len(counts)):
					if counts[index] == 1:
						# this is unique, so occurred once
						snp_positions[vcffilenames[snp_index[index]]][chromosome][position].update({'unique':True}) # vcffilenames[snp_index[index]] =  this will be the filename
						#print("this is unique", vcffilenames[snp_index[index]], chromosome, position, snp_positions[vcffilenames[snp_index[index]]][chromosome][position])


			#else:
			#	vcf_database['snp_positions'][chromosome + "_" + position].update({'unique':False})
	key_counter+=1

	return

def get_common_snps():

	''' Get snps common to all vcf files'''

	for chromosome in snpsites.keys():
		for position in snpsites[chromosome].keys():
			if all(snpsites[chromosome][position]) == True:
				#lets check if all alt bases are same
				alt_snps=[]
				for index in range(len(snpsites[chromosome][position])):
					alt_snps.append(snp_positions[vcffilenames[index]][chromosome][position]['alt'])

				counts = count_list_elements_occurrences(alt_snps)

				for countindex in range(len(counts)):
					if counts[countindex] == len(vcffilenames):
							snp_positions[vcffilenames[countindex]][chromosome][position].update({'common' : True})

				#print(snp_positions[vcffilenames[index]], chromosome, position, set(counts), counts)
				#else:
				#	vcf_database[key]['snp_positions'][chromosome + "_" + positon].update({'common' : True})

def save_display_common_unique_snps(save=True, display=False):
	'save the results to files and/or display the results'
	for filename in vcffilenames:
		outfile=options.outdir + "/" + os.path.basename(filename).replace(".vcf", "") + "_snpanalysis.txt"
		outfh=open(outfile, "w")
		print("Output saved in :", outfile)
		for chromosome in snp_positions[filename].keys():
			for position in snp_positions[filename][chromosome].keys():
				if 'common' in snp_positions[filename][chromosome][position].keys() and snp_positions[filename][chromosome][position]['common'] == True:
					if save == True:
						outfh.write(" ".join([chromosome,position, snp_positions[filename][chromosome][position]['ref'], snp_positions[filename][chromosome][position]['alt'], 'common']) + "\n")
					if display == True:
						print(" ".join([chromosome,position, snp_positions[filename][chromosome][position]['ref'], snp_positions[filename][chromosome][position]['alt'], 'common']))
				elif 'unique' in snp_positions[filename][chromosome][position].keys() and snp_positions[filename][chromosome][position]['unique'] == True:
					if save == True:
						outfh.write(" ".join([chromosome,position, snp_positions[filename][chromosome][position]['ref'], snp_positions[filename][chromosome][position]['alt'], 'unique']) + "\n")
					if display == True:
						print(" ".join([chromosome, position, snp_positions[filename][chromosome][position]['ref'], snp_positions[filename][chromosome][position]['alt'], 'unique']))

		outfh.close()

	return

def main():

	#construct a database of vcf filename and records
	# Read the snps from vcf and filter them one by one.

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

	save_display_common_unique_snps(save=True, display=options.display)

if  __name__ == '__main__':

	options=parser.parse_args()
	if not options.vcf:
		print("Input VCF file/s not provided. Use option --vcf to provde the input VCF files (mutliple vcf files should be space separated)")
		exit(1)
	if len(options.vcf) ==1 and options.compare == True:
		print("Number of VCF files provided : ", len(options.vcf))
		print("SNP compare will not be done.")
		options.compare=False



	vcffilenames  = options.vcf


	main()
exit(0)
