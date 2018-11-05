#!/usr/bin/env python3

## unittest for filter_vcf.py functions

import os, sys
import unittest
rootPath=os.path.dirname(os.path.abspath(sys.argv[0])) + "/.."
cgiPath=rootPath + "/cgi-bin"
sys.path.append(cgiPath)

from filter_vcf import filterVCF as fv

class Test_filter_vcf(unittest.TestCase):
	vcf=rootPath + "/testfiles/Sample1.vcf"
	vcfline = 'tig00000003	775	.	A	G	.	PASS	ADP=8;WT=0;HET=0;HOM=1;NC=0	GT:GQ:SDP:DP:RD:AD:FREQ:PVAL:RBQ:ABQ:RDF:RDR:ADF:ADR	1/1:24:8:8:2:6:75%:3.4965E-3:31:30:2:0:6:0'
	vcfobj = fv(vcf)
	def test_filter_by_genotype(self):
		genotype = self.vcfobj.filter_by_genotype(self.vcfline)
		self.assertEqual(genotype, 'Homozygous')

	def test_filter_by_frequency(self):
		result=self.vcfobj.filter_by_frequency(self.vcfline, 75)
		self.assertGreaterEqual(result,75)
	def test_filter_by_genotype_quality(self):
		result = self.vcfobj.filter_by_genotype_quality(self.vcfline, 24)
		self.assertGreaterEqual(result,24)
	def test_filter_by_raw_read_depth(self):
		result=self.vcfobj.filter_by_raw_read_depth(self.vcfline, 8)
		self.assertGreaterEqual(result,8)
	def test_filter_by_quality_read_depth(self):
		result=self.vcfobj.filter_by_quality_read_depth(self.vcfline, 8)
		self.assertGreaterEqual(result, 8)
	def test_filter_by_ref_support_read_depth(self):
		result=self.vcfobj.filter_by_ref_support_read_depth(self.vcfline, 2)
		self.assertGreaterEqual(result, 2)
	def test_filter_by_variant_support_read_depth(self):
		result=self.vcfobj.filter_by_variant_support_read_depth(self.vcfline, 6)
		self.assertGreaterEqual(result, 6)
	def test_filter_by_pvalue(self):
		result=self.vcfobj.filter_by_pvalue(self.vcfline, 3.4965E-3)
		self.assertLessEqual(result, 3.4965E-3)
	def test_filter_by_reference_support_bases(self):
		result=self.vcfobj.filter_by_reference_support_bases(self.vcfline, 31)
		self.assertGreaterEqual(result,31)
	def test_filter_by_quality_variant_bases(self):
		result=self.vcfobj.filter_by_quality_variant_bases(self.vcfline, 30)
		self.assertGreaterEqual(result,30)
	def test_filter_by_ref_forward_strand(self):
		result=self.vcfobj.filter_by_ref_forward_strand(self.vcfline, 2)
		self.assertGreaterEqual(result,2)
	def test_filter_by_ref_reverse_strand(self):
		result=self.vcfobj.filter_by_ref_reverse_strand(self.vcfline, 0)
		self.assertGreaterEqual(result, 0)
	def test_filter_by_variant_forward_strand(self):
		result=self.vcfobj.filter_by_variant_forward_strand(self.vcfline, 6)
		self.assertGreaterEqual(result, 6)
	def test_filter_by_variant_reverse_strand(self):
		result=self.vcfobj.filter_by_variant_reverse_strand(self.vcfline, 0)
		self.assertGreaterEqual(result,0)
if __name__ == '__main__':
	unittest.main()
