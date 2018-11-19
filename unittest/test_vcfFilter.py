#!/usr/bin/env python3
import sys, os
import unittest

rootPath=os.path.dirname(os.path.abspath(sys.argv[0])) + "/.."
cgiPath=rootPath + "/cgi-bin"
sys.path.append(cgiPath)

from vcfFilter import filter

class test_filter(unittest.TestCase):

	filterobj = filter('testfiles/Sample1.vcf')
	record = filterobj.vcf_reader.next()
	def test_get_record_calldata(self):
		self.filterobj.get_record_calldata(self.record)

	def test_get_pvalue(self):
		pvalue = self.filterobj.get_pvalue()
		self.assertLessEqual(pvalue, 0.00349)

	def test_get_frequency(self):
		frequency = self.filterobject.get_frequency()
		self.assertEqual(frequency, 75)

if __name__== '__main__':
	unittest.main()
