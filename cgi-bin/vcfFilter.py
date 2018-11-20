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
parser.add_argument("--gt", dest="genotype", action="store", default="homozygous", help="Genotype of the SNP")
parser.add_argument("--freq", dest="frequency", action="store", type=int, default= 50, help="frequency of the SNP")
parser.add_argument("--dp", dest="quality_read_depth", action="store", type=int, default=5, help="Filter SNPs with quality read depth")
parser.add_argument("--pvalue", dest="pvalue", action="store", type=float, default=0.05, help="Filter SNPs with pvalue of snp call")
parser.add_argument('--output', '--out', dest='output', action='store', default="vcffilter_output.vcf", help="Output filename")
parser.add_argument('--gq', dest='genotype_quality', action='store', default=10, help='Genotype Quality')
parser.add_argument('--asd', dest='read_quality_depth', action='store', default=3, help='Read Quality Depth')
parser.add_argument('--rrd', dest='raw_read_depth', action='store', default=3, help='Raw read depth as reported by Samtools')
parser.add_argument('--rd', dest='depth_in_reference', action='store', default=3, help='Raw depth in reference')
parser.add_argument('--ad', dest='depth_in_variant', action='store', default=3, help='Raw depth in varaint')

options = parser.parse_args()


class filter():
	'''	A class for filtering SNPs in VCF files	'''
	def __init__(self, vcffilename):
		self.vcffilename = vcffilename
		self.open_vcf()
		return
	def open_vcf(self):
		self.vcf_reader=vcf.Reader(open(self.vcffilename, 'r'))
		return
	def open_vcf_writer(self, out):
		self.vcf_writer=vcf.Writer(open(out, 'w'), self.vcf_reader)

	def write_vcf(self, record):
		self.vcf_writer.write_record(record)
	def get_a_record(self):
		return self.vcf_reader.next()
	def get_samplename(self):
		return self.vcf_reader.samples[0]
	def get_record_calldata(self, record):
		self.recordcall = record.genotype(self.sample)
		return self.recordcall

	def get_frequency(self, record, sample):
		'return frequency of SNP genotype'
		call = record.genotype(sample)
		return float(call.data.FREQ.replace('%', ''))
	def get_pvalue(self,record, sample):
		'return pvalue of a SNP record'
		call = record.genotype(sample)
		return float(call.data.PVAL)
	def get_genotype(self,record, sample):
		'return the genotype of a snp record'
		call=record.genotype(sample)
		genotype=call.data.GT
		array=genotype.split('/')
		if array[0] == array[1]:
			return 'homozygous'
		else:
			return 'heterozygous'

	def get_read_quality_depth(self,record, sample):
		'return the quality read depth for snp record'
		call=record.genotype(sample)
		return int(call.data.DP)
	def get_genotype_quality(self, record, sample):
		'return genotype quality'
		call=record.genotype(sample)
		return int(call.data.GQ)
	# def get_avg_sample_depth(self, record, sample):
	# 	call=record.genotype(sample)
	# 	return int(call.data.ADP)
	def get_raw_read_depth(self, record, sample):
		call=record.genotype(sample)
		return int(call.data.SDP)
	def get_depth_in_reference(self, record, sample):
		call=record.genotype(sample)
		return int(call.data.RD)
	def get_depth_in_variant(self, record, sample):
		call=record.genotype(sample)
		return int(call.data.AD)


	def do_filter(self, genotype, frequency, pvalue, raw_read_depth, quality_read_depth, genotype_quality, depth_in_reference, depth_in_variant):

		samplenames = vcffilter.vcf_reader.samples
		vcffilter.samples = samplenames
		for record in vcffilter.vcf_reader:
			#vcffilter.get_record_calldata(record)
			for samplename in samplenames:
				if vcffilter.get_frequency(record, samplename) >= int(frequency):
					if vcffilter.get_pvalue(record, samplename) <= float(pvalue):
						if genotype == 'both' or vcffilter.get_genotype(record, samplename) == genotype:
							if vcffilter.get_read_quality_depth(record, samplename) >= int(quality_read_depth):
								if vcffilter.get_genotype_quality(record, samplename) >= int(genotype_quality):
									if vcffilter.get_raw_read_depth(record, samplename) >= int(raw_read_depth):
										if vcffilter.get_depth_in_reference(record, samplename) >= int(depth_in_reference):
											if vcffilter.get_depth_in_variant(record, samplename) >= int(depth_in_variant):
												vcffilter.write_vcf(record)


		return




if __name__=='__main__':
	vcffilter=filter(options.input)
	vcffilter.open_vcf_writer(options.output)
	vcffilter.do_filter(options.genotype, options.frequency, options.pvalue, options.raw_read_depth, options.quality_read_depth, options.genotype_quality, options.depth_in_reference, options.depth_in_variant)
