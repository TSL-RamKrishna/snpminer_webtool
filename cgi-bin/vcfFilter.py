#!/usr/bin/env python3
import sys, re
import numpy as np
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
parser.add_argument('--gq', dest='genotype_quality', type=int, action='store', default=10, help='Genotype Quality')
parser.add_argument('--asd', dest='quality_read_depth', type=int, action='store', default=3, help='Read Quality Depth')
parser.add_argument('--rrd', dest='raw_read_depth', type=int, action='store', default=3, help='Raw read depth as reported by Samtools')
parser.add_argument('--rd', dest='depth_in_reference', type=int, action='store', default=3, help='Raw depth in reference')
parser.add_argument('--ad', dest='depth_in_variant', type=int, action='store', default=3, help='Raw depth in varaint')

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
		return call.data.PVAL
	def get_genotype(self,record, sample):
		'return the genotype of a snp record'
		call=record.genotype(sample)
		genotype=call.data.GT
		array=genotype.split('/')
		if array[0] == array[1]:
			return 'homozygous'
		else:
			return 'heterozygous'

	def get_quality_read_depth(self,record, sample):
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
	def check_threshold_value(self, recordvalue, testvalue):
		if recordvalue >= testvalue:
			return True
		else:
			return False

	def check_frequency(self,record, sample, testvalue):
		return self.check_threshold_value(self.get_frequency(record,sample), testvalue)
	def check_pvalue(self, record, sample,testvalue):
		record_pvalue=float(self.get_pvalue(record, sample))
		if record_pvalue <= float(testvalue):
			return True
		else:
			return False
		#return (not self.check_threshold_value(float(self.get_pvalue(record, sample)), np.float32(testvalue)))		# here we are testing pvalue less or equal to, so we have to return the opposite result
	def check_genotype(self,record, sample,testvalue):
		return self.check_threshold_value(self.get_genotype(record, sample), testvalue)
	def check_genotype_quality(self,record, sample,testvalue):
		return self.check_threshold_value(self.get_genotype_quality(record, sample), testvalue)
	def check_quality_read_depth(self, record, sample,testvalue):
		return self.check_threshold_value(self.get_quality_read_depth(record, sample), testvalue)
	def check_raw_read_depth(self,record, sample,testvalue):
		return self.check_threshold_value(self.get_raw_read_depth(record,sample), testvalue)
	def check_depth_in_reference(self,record, sample,testvalue):
		return self.check_threshold_value(self.get_depth_in_reference(record, sample), testvalue)
	def check_depth_in_variant(self,record, sample,testvalue):
		return self.check_threshold_value(self.get_depth_in_variant(record, sample), testvalue)


	def do_filter(self, frequency, pvalue, genotype, genotype_quality, raw_read_depth, quality_read_depth, depth_in_reference, depth_in_variant):


		#test_functions=['check_frequency', 'check_pvalue', 'check_genotype', 'check_genotype_quality', 'check_quality_read_depth', 'check_raw_read_depth', 'check_raw_depth_in_reference', 'check_depth_in_variant']
		count_successful_records=0
		samplenames = self.vcf_reader.samples
		print ('samples', samplenames)
		
		for record in self.vcf_reader:
			#vcffilter.get_record_calldata(record)
			for samplename in samplenames:
				#result=[getattr(self, function)(record, samplename) for funciton in test_functions]
				results=[
						self.check_frequency(record, samplename, frequency),
						self.check_pvalue(record, samplename, pvalue),
						self.check_genotype(record,samplename, genotype),
						self.check_genotype_quality(record,samplename,genotype_quality),
						self.check_quality_read_depth(record, samplename, quality_read_depth),
						self.check_raw_read_depth(record,samplename, raw_read_depth),
						self.check_depth_in_reference(record, samplename, depth_in_reference),
						self.check_depth_in_variant(record, samplename, depth_in_variant)
						]

				if all(results):
					print(count_successful_records)
					print ('writing results', results)
					self.write_vcf(record)
					count_successful_records+=1
		print('returning records ', count_successful_records)
		return count_successful_records




if __name__=='__main__':
	vcffilter=filter(options.input)
	vcffilter.open_vcf_writer(options.output)
	vcffilter.do_filter(options.frequency, options.pvalue, options.genotype, options.genotype_quality, options.raw_read_depth, options.quality_read_depth,  options.depth_in_reference, options.depth_in_variant)
