#!/usr/bin/env python3
import sys, os
import unittest
import vcf

rootPath=os.path.dirname(os.path.abspath(sys.argv[0])) + "/.."
cgiPath=rootPath + "/cgi-bin"
sys.path.append(cgiPath)

from vcfFilter import filter

class test_filter(unittest.TestCase):

	filterobj = filter('testfiles/Sample1.vcf')
	record=filterobj.get_a_record()
	samplename=filterobj.get_samplename()

	def test_get_samplename(self):
		if self.samplename=='':
			self.samplename=self.filterobj.get_samplename()
		self.assertEqual(self.samplename, 'Sample1')

	def test_get_a_record(self):
		if self.record=='':
			self.record=self.filterobj.get_a_record()
		self.assertEqual(type(self.record), vcf.model._Record)

	def test_get_genotype(self):
		self.test_get_a_record(); self.test_get_samplename()
		genotype=self.filterobj.get_genotype(self.record, self.samplename)
		self.assertEqual(genotype, 'homozygous')
	def test_get_pvalue(self):
		self.test_get_a_record(); self.test_get_samplename()
		pvalue = self.filterobj.get_pvalue(self.record, self.samplename)
		self.assertEqual(pvalue, 0.0034965)

	def test_get_frequency(self):
		self.test_get_a_record(); self.test_get_samplename()
		frequency = self.filterobj.get_frequency(self.record, self.samplename)
		self.assertEqual(frequency, 75)

	def test_get_read_quality_depth(self):
		self.test_get_a_record(); self.test_get_samplename()
		self.assertEqual(self.filterobj.get_read_quality_depth(self.record, self.samplename), 8)

	def test_get_raw_read_depth(self):
		self.test_get_a_record(); self.test_get_samplename()
		self.assertEqual(self.filterobj.get_raw_read_depth(self.record, self.samplename), 8)

	def test_get_genotype_quality(self):
		self.test_get_a_record(); self.test_get_samplename()
		self.assertEqual(self.filterobj.get_genotype_quality(self.record, self.samplename), 24)

	def test_get_depth_in_reference(self):
		self.test_get_a_record(); self.test_get_samplename()
		self.assertEqual(self.filterobj.get_depth_in_reference(self.record, self.samplename), 2)

	def test_get_depth_in_variant(self):
		self.test_get_a_record(); self.test_get_samplename()
		self.assertEqual(self.filterobj.get_depth_in_variant(self.record, self.samplename), 6)

	def test_open_vcf_writer(self):
		self.test_get_a_record(); self.test_get_samplename()
		self.assertIsNone(self.filterobj.open_vcf_writer('testfiles/unittest_filter_output.vcf'))

	def test_write_vcf(self):
		self.test_get_a_record(); self.test_get_samplename()
		self.assertIsNone(self.filterobj.write_vcf(self.record))

if __name__== '__main__':
	unittest.main()
