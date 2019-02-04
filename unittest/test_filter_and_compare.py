#!/usr/bin/env python3
import sys, os
import numpy as np
import unittest
import vcf

rootPath=os.path.dirname(os.path.abspath(sys.argv[0])) + "/.."
cgiPath=rootPath + "/cgi-bin"
scriptPath=rootPath + "/scripts"
sys.path.append(cgiPath)
sys.path.append(scriptPath)

import filter_and_comparesnps

filter_and_comparesnps.vcffilenames=['testfiles/test1.vcf', 'testfiles/test2.vcf']

class test_filter_and_comparesnps(unittest.TestCase):

	def test_filter_snps(self):
		snpsites={'tig00000003': {'775': [True, True], '776': [True, True], '836': [True, True], '1077': [False, False]}, 'tig00000004': {'1166': [True, True], '1190': [True, True]}}
		filter_and_comparesnps.filter_snps(True)
		self.assertEqual(snpsites,filter_and_comparesnps.snpsites)

	def test_filter_vcf_records(self):
		recordFilter=filter_and_comparesnps.filter_vcf_records()
		vcf_reader=vcf.Reader(open('testfiles/test1.vcf'), 'rb')
		record=next(vcf_reader)
		samplename= vcf_reader.samples[0]
		recordFilter.set_record(record, samplename)
		self.assertTrue(recordFilter.filter_a_record())

	def test_restest_filter_vcf_records(self):
		recordFilter=filter_and_comparesnps.filter_vcf_records(genotype_quality=100)
		vcf_reader=vcf.Reader(open('testfiles/test1.vcf'), 'rb')
		record=next(vcf_reader)
		samplename= vcf_reader.samples[0]
		recordFilter.set_record(record, samplename)
		self.assertFalse(recordFilter.filter_a_record())

	def test_count_list_elements_occurrences(self):
		count_bases=filter_and_comparesnps.count_list_elements_occurrences(['A', 'A','C', 'C,T', 'T', 'G','G'])
		self.assertEqual(count_bases, [2,2,1,1,1,2,2])

	def test_get_unique_snps(self):
		recordFilter=filter_and_comparesnps.filter_vcf_records()
		filter_and_comparesnps.filter_snps(True)
		filter_and_comparesnps.get_unique_snps()
		unique_snps = {'testfiles/test1.vcf': {'tig00000003': {'775': {'ref': 'A', 'alt': 'G'}, '776': {'ref': 'T', 'alt': 'C'}, '836': {'ref': 'G', 'alt': 'C', 'unique': True}},
						'tig00000004': {'1166': {'ref': 'G', 'alt': 'A'}, '1190': {'ref': 'G', 'alt': 'A', 'unique': True}}},
						'testfiles/test2.vcf': {'tig00000003': {'775': {'ref': 'A', 'alt': 'G'}, '776': {'ref': 'T', 'alt': 'C'}, '836': {'ref': 'G', 'alt': 'T', 'unique': True}},
						'tig00000004': {'1166': {'ref': 'G', 'alt': 'A'}, '1190': {'ref': 'G', 'alt': 'A,C', 'unique': True}}}}

		self.assertEqual(unique_snps,  filter_and_comparesnps.snp_positions)
	def test_get_common_snps(self):
		common_snps = {'testfiles/test1.vcf': {'tig00000003': {'775': {'ref': 'A', 'alt': 'G', 'common': True}, '776': {'ref': 'T', 'alt': 'C', 'common': True}, '836': {'ref': 'G', 'alt': 'C'}},
					'tig00000004': {'1166': {'ref': 'G', 'alt': 'A', 'common': True}, '1190': {'ref': 'G', 'alt': 'A'}}},
					'testfiles/test2.vcf': {'tig00000003': {'775': {'ref': 'A', 'alt': 'G', 'common': True}, '776': {'ref': 'T', 'alt': 'C', 'common': True}, '836': {'ref': 'G', 'alt': 'T'}},
					'tig00000004': {'1166': {'ref': 'G', 'alt': 'A', 'common': True}, '1190': {'ref': 'G', 'alt': 'A,C'}}}}
		recordFilter=filter_and_comparesnps.filter_vcf_records()
		filter_and_comparesnps.filter_snps(True)
		filter_and_comparesnps.get_common_snps()
		self.assertEqual(common_snps, filter_and_comparesnps.snp_positions)

	def test_save_display_common_unique_snps(self):
		self.assertTrue(filter_and_comparesnps.save_display_common_unique_snps, None)



if __name__=='__main__':
	unittest.main()
