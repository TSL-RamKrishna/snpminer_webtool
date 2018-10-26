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


class filterVCF():
	'''
	A class for filtering SNPs in VCF files
	'''

	def __init__(self, vcf):
		self.vcf_reader = open(vcf, 'r')

	def read_vcf(self):
		self.vcfline=self.vcf_reader.readline()
		return self.vcfline


	def filter_by_genotype(self):
		line=self.read_vcf()
		if options.genotype in line:
			return True
		else:
			return False

	def filter_by_frequency(self):
		asdf
	def filter_by_allele_depth(self):
		asdf
	def filter_by_genotype_quality(self):
		asdf
	def filter_by_raw_read_depth(self):
		asdf
	def filter_by_quality_read_depth(self):
		asdf
	def filter_by_ref_support_read_dpeth(self):
		asdf
	def filter_by_variant_support_read_dpeth(self):
		asdf
	def filter_by_pvalue(self):
		asdf
	def filter_by_reference_support_bases(self):
		asdf
	def filter_vy_quality_variant_bases(self):
		asdf
	def filter_by_ref_forward_strand(self):
		asdf
	def filter_by_ref_reverse_strand(self):
		asdf
	def filter_vy_variant_forward_strand(self):
		asdf
	def filter_by_variant_reverse_strand(self):
		asdf



def filtersnps_by_position(positions, reflength):

    # min array size should be 3.
    selected_positions = []
    positions=sorted(map(lambda x:int(x), positions)) # incase there are string numbers
    if len(positions) ==1:
        if positions[0] >= min_distance_between_snps and reflength - min_distance_between_snps >= positions[0]:
            selected_positions.append(positions[0])
    elif len(positions) == 2:
        if positions[1] - positions[0] > 200:
            if positions[0] >= min_distance_between_snps:
                selected_positions.append(positions[0])
            if reflength - min_distance_between_snps >= positions[1]:
                selected_positions.append(positions[1])
    elif len(positions) >=3:

        #if positions[0] > min_distance_between_snps and positions[1] - positions[0] >= min_distance_between_snps:
        if positions[1] - positions[0] >= min_distance_between_snps:
            selected_positions.append(positions[0])

        for pos in range(1, len(positions)-1):
            if positions[pos] - positions[pos-1] > min_distance_between_snps and positions[pos+1] - positions[pos] > min_distance_between_snps:
                selected_positions.append(positions[pos])

        #if reflength - min_distance_between_snps > positions[-1] and positions[-1] - positions[-2] > min_distance_between_snps:
        if positions[-1] - positions[-2] > min_distance_between_snps:
            selected_positions.append(positions[-1])

    return selected_positions

def get_highest_dp(vcfline):
    dparray=re.findall('DP\d*=\d{1,10}', vcfline)
    highest_dp=sorted(map(lambda x: int(x.split("=")[1]), dparray), reverse=True)[0]
    return highest_dp


def main(ref_lengths, vcf_file, filtered_vcf_file):

    readlengthfh=open(ref_lengths)      # File with reference sequences and their lengths
    readlengths=dict()
    for line in readlengthfh:
        line=line.rstrip()
        if line=="":
            continue
        else:
            linearray=line.split()
            readlengths[linearray[0]] = int(linearray[1])

    readlengthfh.close()

    vcfhandle=open(vcf_file)     #VCF file after comparing Sparent and Sbulk with Rparent

    filtersnps=dict()
    for line in vcfhandle:
        line=line.rstrip()
        if line=="":
            continue
        else:
            reference = line.split()[0]
            position = int(line.split()[1])
            if reference in filtersnps.keys():
                filtersnps[reference]["positions"].append(position)
            else:
                filtersnps[reference]={"positions":[position]}

    vcfhandle.close()

    # lets select positions with snps that has no snps around 200 positions

    for refseqkey in filtersnps.keys():
        #print filtersnps[refseqkey]["positions"]
        #print readlengths[refseqkey]
        selected_positions = filtersnps_by_position(filtersnps[refseqkey]["positions"], readlengths[refseqkey])
        filtersnps[refseqkey]["selected_positions"]=selected_positions

    # now we have selected the positions, lets get the snps from vcf file if read depth is above minimum threshold
    vcfhandle=open(vcf_file)
    output = open(filtered_vcf_file, "w")
    for vcfline in vcfhandle:
        vcfline=vcfline.rstrip()
        if line=="":
            continue
        else:
            reference = vcfline.split()[0]
            position = int(vcfline.split()[1])
            if get_highest_dp(vcfline) >=min_dp_threshold:
                if position in filtersnps[reference]["selected_positions"]:
                    output.write(vcfline + "\n")
            else:
                continue

    vcfhandle.close()
    output.close()

if __name__ ==  "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
exit(0)
