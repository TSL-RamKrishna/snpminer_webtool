#!/usr/bin/env python3

# Program to verify VCF file

import os, sys

class verify_vcf():

	def __init__(self, vcf):
		self.vcf=vcf
		self.vcf_handle=open(self.vcf, 'r')
	def readline_vcf(self):
		return self.vcf_handle.readline()

	def verify_firstline(self):
		line=self.readline_vcf()
		if line.startswith("##fileformat=VCFv4."):
			pass
		else:
			print("VCF first line does not start with ##fileformat=VCFv4")
			return False
		return True

	def verify(self):

		counter = 0
		if self.verify_firstline() == True:
			pass
		else:
			return "VCF format verification failed. The first line need to begin with - ##fileformat=VCFv4.x"
		while True:
			line=self.readline_vcf()
			if line.startswith('##source=') or line.startswith('##INFO=') or line.startswith('##FILTER=') or line.startswith('##FORMAT='):
				pass
			elif line.startswith('#CHROM'):
				header = line.split("\t")
				if len(header)>=10:		# the number of columns in header has to be 10 or more including at least one sample
					if " ".join(header[:-1]) == "#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT":
						pass
					else:
						print()
						return "VCF format verification failed. The header line should have the columns: #CHROM POS ID REF ALT QUAL FILTER INFO FORMAT and at least a sample"


			elif line.startswith("##"):
				pass
			else:
				return "VCF format verifcation passed"


if __name__=='__main__':
	verification = verify_vcf(sys.argv[1])
	print(verification.verify())
