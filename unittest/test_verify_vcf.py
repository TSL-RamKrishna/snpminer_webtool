#!/usr/bin/env python3

# uniittest for vcf verification
import os, sys
import unittest
rootPath=os.path.dirname(os.path.abspath(sys.argv[0])) + "/.."
cgiPath=rootPath + "/cgi"
sys.path.append(cgiPath)

from verify_vcf import verify_vcf as vv

class Test_verify_vcf(unittest.TestCase):

	def test_verify(self, vcf=rootPath + "/testfiles/Sample1.vcf"):

		vcfobj = vv(vcf)
		result = vcfobj.verify()
		self.assertEqual(result, "VCF format verifcation passed")


if __name__ == '__main__':
	unittest.main()
