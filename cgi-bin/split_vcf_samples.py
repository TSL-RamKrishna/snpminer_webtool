#!/usr/bin/env python3

import os, sys

inputvcf = open(sys.argv[1], 'r')
samplename_to_split=sys.argv[2]

def samplename_column(data, samplename):
    # function to get the column number of the sample
    array = data.split()
    for position in range(len(array)):
        if array[position] == samplename:
            break
    return position

for line in inputvcf:
    line=line.rstrip()
    if line == "":
        continue
    elif line.startswith('##'):
        print(line)
    elif line.startswith('#CHROM'):
        # header line
        samplename_column_number = samplename_column(line, samplename_to_split)
        headers=line.split()
        print("\t".join(headers[:9]) + "\t" + headers[samplename_column_number])
    else:
        record=line.split()
        print("\t".join(record[0:9]) + "\t" + record[samplename_column_number])


exit(0)
