#!/usr/bin/env python3
import sys, re
import argparse
import vcf
#############################
### program to filter VCF snps with following filter criteria
### 1) snp position should not have another snp 200 bp forward or backward
### 2) min depth = 100
#############################
### usage : python scriptname refseq.lengths vcf.filename outputfilename


parser=argparse.ArgumentParser(description="Filter vcf", version="0.01")
parser.add_argument("-i", "--input", dest="input", action="store", help="VCF input file")
parser.add_argument("--gt", dest="genotype", action="store", default="Heterozygous", help="Genotype of the SNP")
parser.add_argument("--freq", dest="frequency", action="store", help="frequency of the SNP")
parser.add_argument("--adp", dest="adp", action="store", help="allele depth")
parser.add_argument("--gp", dest="genotype_quality", action="store", help="Genotype quality value to filter SNPs")
parser.add_argument("--sdp", dest="raw_read_depth", action="store", help="Filter SNPs with Raw Read Depth value")
parser.add_argument("--dp", dest="quality_read_depth", action="store", help="Filter SNPs with quality read depth")
parser.add_argument("--rd", dest="ref_support_read_depth", action="store", help="Filter SNPs with reference support read depth")
parser.add_argument("--ad", dest="variant_support_read_depth", action="store", help="Filter SNPs with variant support read depth")
parser.add_argument("--pvalue", dest="pvalue", action="store", help="Filter using Pvalue of the SNPs")
parser.add_argument("--rbq", dest="reference_support_bases", action="store", help="Filter using number of reference support bases")
parser.add_argument("--abq", dest="quality_variant_bases", action="store", help="Filter using average of quality variant support bases")
parser.add_argument("--rdf", dest="ref_forward_strand", action="store", help="Filter using depth of reference support forward strand")
parser.add_argument("--rdr", dest="ref_reverse_strand", action="store", help="Filter using depth of reference support reverse strand")
parser.add_argument("--adf", dest="variant_forward_strand", action="store", help="Filter using depth of variant support forward strand")
parser.add_argument("--adr", dest="variant_reverse_strand", action="store", help="Filter using depth of variant support reverse strand")
parser.add_argument("--more-filter", dest="more-filter", action="store", default=None, help="More filter options")

options=parser.parse_args()
class filterVCF():
	'''
	A class for filtering SNPs in VCF files
	'''

	def __init__(self, vcf):
		self.vcf_reader = open(vcf, 'r')

	def read_vcf(self):
		self.vcfline=self.vcf_reader.readline()
	def close_vcf(self):
		self.vcf_reader.close()
	def get_format(self, line):
		return line.split("\t")[8]
	def get_info(self, line):
		return line.split("\t")[7]
	def get_format_key_position(self, vcfline, idname):

		format = self.get_format(vcfline)
		counter=0
		for key in format.split(":"):
			if key ==idname.upper():
				return counter
			else:
				counter+=1
		return "unknown format ID"

	def get_sample_value_for_format_key(self, vcfline, counter):
		sampledata = vcfline.split('\t')[9]
		return sampledata.split(":")[counter]

	def filter_by_genotype(self, vcfline):

		position = self.get_format_key_position(vcfline, 'GT')
		genotype = self.get_sample_value_for_format_key(vcfline, position)
		alleles = genotype.split("/")
		if len(alleles) == 2:
			if alleles[0] == alleles[1]:
				return 'Homozygous'
			else:
				return 'Heterozygous'
		elif len(alleles) == 3:
			if alleles[0] == alleles[1] == alleles[2]:
				return 'Homozygous'
			else:
				return 'Heterozygous'
		else:
			pass


	def filter_by_frequency(self, vcfline, threshold):
		position = self.get_format_key_position(vcfline,'FREQ')
		frequency = self.get_sample_value_for_format_key(vcfline, position).replace('%', '')
		return int(frequency)

	def filter_by_allele_depth(self,vcfline, threshold):
		'filter by allele depth'
		position = self.get_format_key_position(vcfline,'ADP')
		alleleDepth = self.get_sample_value_for_format_key(vcfline, position)
		return int(alleleDepth)

	def filter_by_genotype_quality(self,vcfline, threshold):
		'filter by Genotype Quality'
		position = self.get_format_key_position(vcfline,'GQ')
		genotypeQuality = self.get_sample_value_for_format_key(vcfline, position)
		return int(genotypeQuality)

	def filter_by_raw_read_depth(self,vcfline, threshold):
		'filter by Raw Read Depth as reported by used software tool e.g. SAMtools'
		position = self.get_format_key_position(vcfline,'SDP')
		rawReadDepth = self.get_sample_value_for_format_key(vcfline, position)
		return int(rawReadDepth)

	def filter_by_quality_read_depth(self,vcfline, threshold):
		'filter by Quality Read Depth of bases with Phred score >= 15'
		position = self.get_format_key_position(vcfline,'DP')
		qualityReadDepth = self.get_sample_value_for_format_key(vcfline, position)
		return int(qualityReadDepth)

	def filter_by_ref_support_read_depth(self,vcfline, threshold):
		'filter by the sample Depth of reference-supporting bases (reads1)'
		position = self.get_format_key_position(vcfline,'RD')
		refSupportReadDepth = self.get_sample_value_for_format_key(vcfline, position)
		return int(refSupportReadDepth)

	def filter_by_variant_support_read_depth(self,vcfline, threshold):
		'filter by the sample Depth of variant-supporting bases (reads2)'
		position = self.get_format_key_position(vcfline,'AD')
		varSupportReadDepth = self.get_sample_value_for_format_key(vcfline, position)
		return int(varSupportReadDepth)
	def filter_by_pvalue(self,vcfline, threshold):
		'filter by P-value from Fisher\'s Exact Test'
		position = self.get_format_key_position(vcfline,'PVAL')
		pvalue = self.get_sample_value_for_format_key(vcfline, position)
		return float(pvalue)

	def filter_by_reference_support_bases(self, vcfline, threshold):
		'filter by Average quality of reference-supporting bases (qual1)'
		position = self.get_format_key_position(vcfline, 'RBQ')
		refSupportBases = self.get_sample_value_for_format_key(vcfline, position)
		return int(refSupportBases)

	def filter_by_quality_variant_bases(self, vcfline, threshold):
		'filter by Average quality of variant-supporting bases (qual2)'
		position = self.get_format_key_position(vcfline,'ABQ')
		variantSupportBases = self.get_sample_value_for_format_key(vcfline, position)
		return int(variantSupportBases)

	def filter_by_ref_forward_strand(self,vcfline, threshold):
		'filter by sample Depth of reference-supporting bases on forward strand (reads1plus)'
		position = self.get_format_key_position(vcfline,'RDF')
		refForwardStrand = self.get_sample_value_for_format_key(vcfline, position)
		return int(refForwardStrand)

	def filter_by_ref_reverse_strand(self, vcfline, threshold):
		'filter by sample Depth of reference-supporting bases on reverse strand (reads1minus)'
		position = self.get_format_key_position(vcfline,'RDR')
		refReverseStrand = self.get_sample_value_for_format_key(vcfline, position)
		return int(refReverseStrand)

	def filter_by_variant_forward_strand(self, vcfline, threshold):
		'filter the sample by Depth of variant-supporting bases on forward strand (reads2plus)'
		position = self.get_format_key_position(vcfline,'ADF')
		variantForwardStrand = self.get_sample_value_for_format_key(vcfline, position)
		return int(variantForwardStrand)

	def filter_by_variant_reverse_strand(self, vcfline, threshold):
		'filter the sample by Depth of variant-supporting bases on reverse strand (reads2minus)'
		position = self.get_format_key_position(vcfline,'ADR')
		variantReverseStrand = self.get_sample_value_for_format_key(vcfline, position)
		return int(variantReverseStrand)

	def filter(self):
		'filter vcf'

		while True:
			self.read_vcf()
			if not self.vcfline:
				break
			elif self.vcfline.startswith("#"):
				continue
			else:
				if filter_by_genotype(self.vcfline) == options.genotype:
					pass
				else:
					continue
				if filter_by_genotype_quality(self.vcfline) >= options.genotype_quality:
					pass
				else:
					continue
				if filter_by_raw_read_depth(self.vcfline) >= options.raw_read_depth:
					pass
				else:
					continue
				if filter_by_quality_read_depth(self.vcfline) >= options.quality_read_depth:
					pass
				else:
					continue
				if filter_by_ref_support_read_depth(self.vcfline) >= options.ref_support_read_depth:
					pass
				else:
					continue
				if filter_by_variant_support_read_depth(self.vcfline) >= options.variant_support_read_depth:
					pass
				else:
					continue
				if filter_by_frequency(self.vcfline) >= options.frequency:
					pass
				else:
					continue
				if filter_by_pvalue(self.vcfline) <= options.pvalue :
					pass
				else:
					continue
				if filter_by_reference_support_bases(self.vcfline) >= options.reference_support_bases:
					pass
				else:
					continue
				if filter_by_variant_support_read_depth(self.vcfline) >= options.variant_support_read_depth:
					pass
				else:
					continue
				if filter_by_ref_forward_strand(self.vcfline) >= options.ref_forward_strand:
					pass
				else:
					continue
				if filter_by_ref_reverse_strand(self.vcfline) >= options.ref_reverse_strand:
					pass
				else:
					continue
				if filter_by_variant_forward_strand(self.vcfline) >= options.variant_forward_strand:
					pass
				else:
					continue
				if filter_by_variant_reverse_strand(self.vcfline) >= options.variant_reverse_strand:
					pass
				else:
					continue
			print(self.vcfline)

if __name__ ==  "__main__":
	filtering = filterVCF(options.input)
	filtering.filter()
