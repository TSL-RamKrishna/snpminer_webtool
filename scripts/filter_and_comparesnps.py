#!/usr/bin/env python3
import os, sys, re
import argparse
import vcf

rootPath=os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(rootPath)

from vcfFilter import filter

parser=argparse.ArgumentParser(description="Script to filter the SNPs using user threshold values and compare the SNPs from multiple VCF files")

parser.add_argument("--vcf", action="store", dest="vcf", nargs="+", help="Space separated vcf input files")
parser.add_argument("--filter", action="store_true", dest="filter", default=False, help="Filter the SNPs")
parser.add_argument("--compare", action="store_true", dest="compare", default=False, help="Compare the SNPs")
parser.add_argument("--frequency", action="store", dest="frequency", default=70, type=int, help="Frequency of SNP call. Default: 70 [int]")
parser.add_argument("--pvalue", action="store", dest="pvalue", default=0.05, type=float, help="Pvalue of the SNP call. Default: 0.05 [float]" )
parser.add_argument("--genotype", action="store", dest="genotype", default="heterozygous", type=str, help="Genotype of the SNP call - heterozygous/homozygous/both. Default: heterozygous")
parser.add_argument("--quality", action="store", dest="genotype_quality", default=10, type=int, help="Genotype quality of the SNP call. Default: 10")
parser.add_argument("--rawreaddepth", action="store", dest="raw_read_depth", default=5, type=int, help="Raw read depth of the SNP call. Default: 5")
parser.add_argument("--qualityreaddepth", action="store", dest="quality_read_depth", default=5, type=int, help="Quality read depth of the SNP call. Default: 5")
parser.add_argument("--depthreference", action="store", dest="depth_in_reference", default=5, type=int, help="Depth in reference of the SNP call. Default: 5")
parser.add_argument("--depthvariant", action="store", dest="depth_in_variant", default=5, type=int, help="Depth in variant of the SNP call. Default: 5")
parser.add_argument("--show", action="store_true", dest="display", default=False, help="Display the results on the screen")
parser.add_argument("--outdir", action="store", dest="outdir", default=os.path.abspath("."), help="Path to the output folder. Default: Current working directory")



snpsites={}		# declare a dict type to store chromosome and snp positions from all vcfs
snp_positions={}	# stores chromosome, position, ref and alt for each vcf file
vcffilenames=[]


class filter_vcf_records():
	"""
	a class to filter the vcf SNP records based on the thresholds provided
	"""

	def __init__(self, frequency=70, pvalue=0.05, genotype="heterozygous", genotype_quality=10, raw_read_depth=1, quality_read_depth=1, depth_in_reference=1, depth_in_variant=1):
		""" Initializes the filter parameters with default values, if not provided
			args:
				:type frequency: int
				:param frequency: Frequency of the ALT base in the SNP position

				:type pvalue: float
				:param pvalue: pvalue of the SNP call

				:type genotype: string
				:param genotype: genotype call heterozygous or homozygous of the SNP

				:type genotype_quality: int
				:param genotype_quality: quality value of the genotype

				:type raw_read_depth: int
				:param raw_read_depth: Raw read depth in the SNP call

				:type quality_read_depth: int
				:param quality_read_depth: Quality Read Depth of bases with Phred score >= 15

				:type depth_in_reference: int
				:param depth_in_reference: depth in reference supporting bases (read1)

				:type depth_in_variant: int
				:param depth_in_variant: depth in variant supporting bases (read2)
			returns:
				None
		"""
		self.filter=filter(frequency, pvalue, genotype, genotype_quality, raw_read_depth, quality_read_depth, depth_in_reference, depth_in_variant)

	def set_filename(self, vcf):
		"""
			sets the VCF filename
			:type vcf: string
			:param vcf: VCF filename

			returns:
				None
		"""
		self.vcf=vcf

	def set_record(self, record, samplename):
		""" set a SNP record and record samplename
		:type record: pyVCF object
		:param record: a SNP record in a VCF file

		:type samplename: string
		:param samplename: name of a sample in the SNP call

		returns:
			None
		"""
		self.record=record
		self.samplename = samplename

	def filter_records(self):

		""" (obsolete now) Filters all SNP records from a vcf filename
			returns: list of pyvcf SNP objects that have passed the filter
		"""

		filter = self.filter.get_passed_filter_records(self.vcf, self.frequency, self.pvalue, self.genotype, self.genotype_quality, self.raw_read_depth, self.quality_read_depth, self.depth_in_reference, self.depth_in_variant)

	def filter_a_record(self):

		""" Filters one SNP record at a time """

		return self.filter.passed_filter(self.record, self.samplename)

def filter_snps(do_filter=False):
	"""
		Filter the snps using threshold values as defined and populates the global variable to with SNP records

		:type do_filter: boolean
		:param do_filter: decision to filter the SNPs or not

		return:
			None
	"""



	def create_db_for_all_snps(chromosome, position ):
		"""
			records all chromosome and positions in global variable (dictionary data structure) and initializes with an array of False boolean values for each vcf input file
			Each boolean value is a positional value of a snp in input vcf files in an array.
			E.g. if input vcf files are ["test1.vcf", "test2.vcf", "test3.vcf"]
			snpsites["chr1"]["1"] = [False, False, False]
			snpsites["chr1"]["10"] = [False, False, False]
			snpsites["chr2"]["1"] = [False, False, False]

			:type chromosome: string
			:param chromosome: name of the chromosome

			:type position: int
			:param position: position of SNP call in the chromosome

			return:
				None

		"""

		if  chromosome in snpsites.keys():
			if str(position) in snpsites[chromosome].keys():
				return
			else:
				snpsites[chromosome][str(position)] = [False] * len(vcffilenames)
		else:
			snpsites.update({chromosome:{str(position): [False] * len(vcffilenames) }})

	def add_snp_to_database(filename, chromosome, position, ref, alt):
		"""
			append the snp records to the dictionary data structure once they passed the filter

			:type filename: string
			:param filename: vcf filename

			:type chromosome: string
			:param chromosome: chromosome name on which SNP was call

			:type position: int
			:param position: base position in the chromosome

			:type ref: String
			:param ref: reference base in SNP call

			:type alt: String
			:param alt: alternate base in SNP call

			return:
				None

		"""

		if filename in snp_positions.keys():
			if chromosome in snp_positions[filename].keys():
				snp_positions[filename][chromosome].update({str(position):{"ref":ref, "alt":str(alt).replace("[","").replace("]", "").replace(" ", "")}} )
			else:
				snp_positions[filename].update({chromosome:{str(position):{"ref":ref, "alt":str(alt).replace("[","").replace("]", "").replace(" ", "")}}})
		else:
			snp_positions.update({filename:{chromosome:{str(position) : {"ref": ref, "alt":str(alt).replace("[","").replace("]", "").replace(" ", "")}}}})

	key_counter = 0
	inputvcf = filter_vcf_records()	# class instance for filtering
	for filename in  vcffilenames:
		vcf_reader=vcf.Reader(open(filename), "rb")
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
					#snp_positions.update({str(key_counter) + "_" + chromosome + "_" + str(position):{"ref": str(ref), "alt":str(alt).replace("[","").replace("]", "")}})
					snpsites[chromosome][str(position)][key_counter] = True
				else:
					pass

			else:
				add_snp_to_database(filename, chromosome, position, ref, alt)
				#snp_positions.update({str(key_counter) + "_" + chromosome + "_" + str(position):{"ref": str(ref), "alt":str(alt).replace("[","").replace("]", "")}})
				snpsites[chromosome][str(position)][key_counter]= True

		key_counter+=1

def count_list_elements_occurrences(alt_bases):
	"""
		counts number of each element of input array

		:type alt_bases: Array
		:param alt_bases: alternate bases from all VCF files for same chromosome and position. e.g. ["A", "T", "A", "T,C"]

		return:
			array with count of each element in the input array. e.g for above array it retuns [2, 1, 2, 1]

	"""
	counts=[]
	for x in alt_bases:
		counts.append(alt_bases.count(x))
	return counts

def get_unique_snps():
	""" records a unique snps in a vcf file """

	key_counter = 0

	for chromosome in snpsites.keys():
		for position in snpsites[chromosome].keys():
			if snpsites[chromosome][position][key_counter] == True and sum(snpsites[chromosome][position]) == 1:  # First any(array) finds first True and second any(array) finds another True, if second True, it will say False
				# This is unique snp

				#vcf_database[key]["unique_snps"].append([chromosome, position, vcf_database[key]["snp_positions"][chromosome + "_" + position]["ref"], ",".join(vcf_database[key]["snp_positions"][chromosome + "_" + position]["alt"]) ])
				snp_positions[vcffilenames[key_counter]][chromosome][position].update({"unique":True})
			elif sum(snpsites[chromosome][position]) >=2:		# there might be snp at same position but with different alt base

				snp_index = [i for i, j in enumerate(snpsites[chromosome][position]) if j==True]

				totalindex = len(snp_index)
				# Lets check the alt base in these vcf files using index
				# lets get array of alt bases from each file
				alt_snps=[]
				for index in snp_index:
					alt_snps.append(snp_positions[vcffilenames[index]][chromosome][position]["alt"])

				# get the counts of the elements

				counts = count_list_elements_occurrences(alt_snps)

				for index in range(len(counts)):
					if counts[index] == 1:
						# this is unique, so occurred once
						snp_positions[vcffilenames[snp_index[index]]][chromosome][position].update({"unique":True}) # vcffilenames[snp_index[index]] =  this will be the filename
						#print("this is unique", vcffilenames[snp_index[index]], chromosome, position, snp_positions[vcffilenames[snp_index[index]]][chromosome][position])


			#else:
			#	vcf_database["snp_positions"][chromosome + "_" + position].update({"unique":False})
	key_counter+=1
	return

def get_common_snps():

	""" records SNPs common to all VCF input files """

	for chromosome in snpsites.keys():
		for position in snpsites[chromosome].keys():
			if all(snpsites[chromosome][position]) == True:
				#lets check if all alt bases are same
				alt_snps=[]
				for index in range(len(snpsites[chromosome][position])):
					alt_snps.append(snp_positions[vcffilenames[index]][chromosome][position]["alt"])

				counts = count_list_elements_occurrences(alt_snps)

				for countindex in range(len(counts)):
					if counts[countindex] == len(vcffilenames):
							snp_positions[vcffilenames[countindex]][chromosome][position].update({"common" : True})


def save_display_common_unique_snps(outdir, save=True, display=False):
	"""
		save the common/unique snps to files and/or display the results

		:type outdir: string
		:param outdir: output directory to save the output files

		:type save: boolean
		:param save: save the results to output files. Default True

		:type display: boolean
		:param display: display the results on the screen. Default False

		returns:
			None
	"""
	outfiles=[]
	for filename in vcffilenames:
		outfile=outdir + "/" + os.path.basename(filename).replace(".vcf", "") + "_snpanalysis.txt"
		outfh=open(outfile, "w"); outfiles.append(outfile)
		if display == True:
			print("Common and Unique SNPS in vcf File : ", filename)
		else:
			print("Common and Unique SNPs from file ", filename , " are saved in :", outfile)
		for chromosome in snp_positions[filename].keys():
			for position in snp_positions[filename][chromosome].keys():
				if "common" in snp_positions[filename][chromosome][position].keys() and snp_positions[filename][chromosome][position]["common"] == True:
					if save == True:
						outfh.write(" ".join([chromosome,position, snp_positions[filename][chromosome][position]["ref"], snp_positions[filename][chromosome][position]["alt"], "common"]) + "\n")
					if display == True:
						print(" ".join([chromosome,position, snp_positions[filename][chromosome][position]["ref"], snp_positions[filename][chromosome][position]["alt"], "common"]))
				elif "unique" in snp_positions[filename][chromosome][position].keys() and snp_positions[filename][chromosome][position]["unique"] == True:
					if save == True:
						outfh.write(" ".join([chromosome,position, snp_positions[filename][chromosome][position]["ref"], snp_positions[filename][chromosome][position]["alt"], "unique"]) + "\n")
					if display == True:
						print(" ".join([chromosome, position, snp_positions[filename][chromosome][position]["ref"], snp_positions[filename][chromosome][position]["alt"], "unique"]))

		outfh.close()
	if display==True:
		print("The outputs are saved in these files :", " ".join(outfiles))

	return

def main(outdir, display, filter=True, compare=False):

	""" the main function to filter SNPs, compare SNPs and to display/save the common and unique SNPs
		:type outdir: String
		:param outdir: output directory to save the output files

		:type display: boolean
		:param display: display results on the screen

		:type filter: boolean
		:param filter: Filter SNPs. Default True

		:type compare: boolean
		:param compare: compare SNPs. Default False

		returns:
			None
	"""

	if filter == True:
		filter_snps(True)
	else:
		filter_snps(False)

	if compare == True:
		get_unique_snps()
		get_common_snps()

	save_display_common_unique_snps(outdir, save=True, display=display)

if  __name__ == "__main__":


	options=parser.parse_args()
	if not options.vcf:
		print("Input VCF file/s not provided. Use option --vcf to provde the input VCF files (mutliple vcf files should be space separated)")
		exit(1)
	if len(options.vcf) ==1 and options.compare == True:
		print("Number of VCF files provided : ", len(options.vcf))
		print("SNP compare will not be done.")
		options.compare=False



	vcffilenames  = options.vcf


	main(options.outdir, options.display, options.filter, options.compare)
	exit(0)
