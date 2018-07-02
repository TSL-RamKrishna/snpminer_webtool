import sys


class filter_vcf_snps():
    ''' class to filter out snps that do not satisfy a criteria '''

    snpdata=dict()

    def __init__(self, vcf):
        self.vcf=vcf

    def __open__(self):
        self.vcfreader=open(self.vcf)
    def __close__(self):
        self.vcfreader.close()
    def __readvcf__(self):

        self.__open__()


        '''
        checks if the vcf file is correctly formatted.
        '''

        fileformat=self.vcfreader.readline()
        if not fileformat.startswith('##fileformat=VCFv4.'):
            print("VCF file should start with ##fileformat=VCFv4.x at the first line, where 4.x is vcf format version")
            exit(1)
        while True:
            description=self.vcfreader.readline().rstrip()
            if description.startswith("##"):
                continue
            else:
                break

        print("Header line ")
        print(description)
        header=description[1:]      #removes # from #CHROM
        number_of_columns_in_header=len(header.split('\t'))
        number_of_samples=number_of_columns_in_header - 9
        samples=header.split("\t")[9:]
        for samplename in samples:
            self.snpdata[samplename]=dict()

        print(number_of_columns_in_header, number_of_samples, samples)

        #read the snps data after header now
        for line in self.vcfreader:
            line=line.rstrip()
            if line == "": continue
            linearray = line.split('\t')
            print linearray
            for samplename in samples:
                self.snpdata[samplename].update({
                'CHROM':linearray[0],
                'POS':linearray[1],
                'ID':linearray[2],
                'REF':linearray[3],
                'ALT':linearray[4],
                'QUAL':linearray[5],
                'FILTER':linearray[6],
                'INFO':linearray[7],
                'FORMAT':
                })



        self.__close__()

    def get_vcf_for_sample(self):
        # get vcf data for selected sample
        pass
    def filter_vcf_by_sample(self):
        #get vcf by sample
        pass
    def filter_vcf_by_no_sample(self):
        # filter out, if one sample does not satisfy a condition
        pass







class compare_vcf_snps():
    ''' compare snps to get common or alternate snps between multiple vcfs '''




vcf1=filter_vcf_snps(sys.argv[1])
vcf1.__readvcf__()
