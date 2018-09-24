#!/usr/bin/python3

import sys, os
from subprocess import Popen, PIPE
# Import modules for CGI handling
import cgi, cgitb

#dir_upload=os.path.dirname(sys.argv[0]) + "/../uploads/"
rootdir = os.path.dirname(sys.argv[0]) + "/../"
dir_upload=rootdir + "uploads/"
dir_process=rootdir + "process/"
log_dir=rootdir + "log"
if not os.path.exists(dir_upload):
	os.makedirs(dir_upload)
if not os.path.exists(dir_process):
	os.makedirs(dir_process)

cgitb.enable(logdir=log_dir)
# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields


resistant_sample_vcfs = form.getvalue('resistant_sample_vcfs')
susceptible_sample_vcfs = form.getvalue('susceptible_sample_vcfs')

reference_sequence = form.getvalue('reference_sequence')
#input_vcfs = form.getvalue("input_vcfs")
filtersnps = form.getvalue("filter-snps")
compare_common = form.getvalue("compare-common")
compare_unique =  form.getvalue("compare-alternate")
genotype = form.getvalue('genotype')
variant_allele_freq = form.getvalue('variant_allele_freq')
per_sample_depth = form.getvalue('per_sample_depth')
sample_called_reference = form.getvalue('sample_called_reference')
not_called = form.getvalue('not_called')
genotype_quality = form.getvalue('genotype_quality')
raw_read_depth = form.getvalue('raw_read_depth')
quality_read_depth = form.getvalue('quality_read_depth')
ref_support_read_depth = form.getvalue('ref_support_read_depth')
variant_read_depth = form.getvalue('variant_read_depth')
variant_called_frequency = form.getvalue('variant_called_frequency')
variant_read_depth = form.getvalue('variant_read_depth')
pvalue =  form.getvalue('pvalue')
avg_qual_ref_support_bases = form.getvalue('avg_qual_ref_support_bases')
avg_qual_variant_support_bases = form.getvalue('avg_qual_variant_support_bases')
depth_ref_support_forward_strand = form.getvalue('depth_ref_support_forward_strand')
depth_ref_support_reverse_strand = form.getvalue('depth_ref_support_reverse_strand')
depth_variant_support_forward_strand = form.getvalue('depth_variant_support_forward_strand')
depth_variant_support_reverse_strand = form.getvalue('depth_variant_support_reverse_strand')


#print(comparesnps, compare)
filter_pythonscript="filter_compare_vcf.py"
compare_common_command="filter_compare_vcf.py"
compare_unique_command="filter_compare_vcf.py"

filter_command="python3 " + filter_pythonscript

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>CGI Program</title>")
print("</head>")
print("<body>")
print("<p>HTML options are below:</p>")
for key in form.keys():
	print("<p>" + key + "</p>")


print("<h2>Data provided are below</h2>")

print("You have input following files:  </br>  </br>")
variable = ""
value = ""
r = ""



reference_sequence = form['reference_sequence'].filename
input_vcfs=[]
if 'input_vcfs' in form:
	filefield=form['input_vcfs']
	if not isinstance(filefield, list):
		print('<p> file instance is not list</p>')
		filefield=[filefield]
	else:
		print('<p>File instance is a list. </p>')

	for fileitem in filefield:
		if fileitem.filename:
			fn=os.path.basename(fileitem.filename)
			input_vcfs.append(fn)
			try:
				with open(dir_upload + fn, 'wb') as fout:
					while True:
						chunk = fileitem.file.read(10000)
						if not chunk:
							break
						fout.write(chunk)
				print('<p>' + fn + " uploaded </p>")

			except:
				print('<p>' + fn + " upload failed </p>")

		else:
			print('<p>' + fn + ' not in the list </p>' )
else:
	print('<p> No Files uploaded </p>')


print("You have selected following parameters:  </br> </br>")


if reference_sequence:
	filter_command+=" --reference " + reference_sequence

if input_vcfs:

	if isinstance(input_vcfs, list):
		filter_command+=" --input " + ",".join(input_vcfs)
	else:
		filter_command+=" --input " + input_vcfs
if filtersnps:
	filter_command+=" --filter "
if compare_common:
	compare_common_command+=" --common "
if compare_unique:
	compare_unique_command+=" --alternate "

if genotype:
	print('Gentotype : {} </br>'.format(genotype))
	filter_command+=" --gt " + str(genotype)
if variant_allele_freq:
	print("Minimum Variant allele frequency (FREQ): {} </br>".format(variant_allele_freq))
	filter_command+=" --freq " + variant_allele_freq
if per_sample_depth:
	print("Minimum Average per-sample depth of bases with Phred score >= 15 (ADP): {} </br>".format(per_sample_depth))
	filter_command+=" --adp " + per_sample_depth
if sample_called_reference:
	print("Minimum Number of samples called reference (wild-type) (WT): {} </br>".format(sample_called_reference))
	filter_command+=" --wt " + sample_called_reference
if not_called:
	print("Minimum Number of samples not called (NC): {} </br>".format(not_called))
	filter_command+=" --nc " + nc_called
if genotype_quality:
	print("Minimum Genotype Quality(GQ): {} </br>".format(genotype_quality))
	filter_command+=" --gq " + genotype_quality
if raw_read_depth:
	print("Minimum Raw Read Depth as reported by SAMtools (SDP): {} </br>".format(raw_read_depth))
	filter_command+=" --sdp " + raw_read_depth
if quality_read_depth:
	print("Minimum Quality Read Depth of bases with Phred score >= 15 (DP) : {} </br>".format(quality_read_depth))
	filter_command+=" --dp " + quality_read_depth
if ref_support_read_depth:
	print("Minimum Depth of reference-supporting bases (reads1) (RD): {}  </br>".format(ref_support_read_depth))
	filter_command+=" --rd " + ref_support_read_depth
if variant_read_depth:
	print("Minimum Depth of variant-supporting bases (reads2) (AD): {}  </br>".format(variant_read_depth))
	filter_command+=" --ad " + variant_read_depth
if pvalue:
	print("P-value from Fisher's Exact Test (PVAL) less or equal to : {} </br>".format(pvalue))
	filter_command+=" --pvalue " + pvalue
if avg_qual_ref_support_bases:
	print("Minimum Average quality of reference-supporting bases (qual1) (RBQ): {} </br>".format(avg_qual_ref_support_bases))
	filter_command+=" --rbq " + avg_qual_ref_support_bases
if avg_qual_variant_support_bases:
	print("Minimum Average quality of variant-supporting bases (qual2) (ABQ):{} </br>".format(avg_qual_variant_support_bases))
	filter_command+=" --abq " + avg_qual_variant_support_bases
if depth_ref_support_forward_strand:
	print("Minimum Depth of reference-supporting bases on forward strand (reads1plus) (RDF): {} </br>".format(depth_ref_support_forward_strand))
	filter_command+=" --rdf " + depth_ref_support_forward_strand
if depth_ref_support_reverse_strand:
	print("Minimum Depth of reference-supporting bases on reverse strand (reads1minus) (RDR): {} </br>" .format(depth_ref_support_reverse_strand))
	filter_command+=" --rdr " + depth_ref_support_reverse_strand
if depth_variant_support_forward_strand:
	print("Minimum Depth of variant-supporting bases on forward strand (reads2plus) (ADF) : {} </br>".format(depth_variant_support_forward_strand))
	filter_command+=" --adf " + depth_variant_support_forward_strand
if depth_variant_support_reverse_strand:
	print("Minimum Depth of variant-supporting bases on reverse strand (reads2minus) (ADR) : {} </br>".format(depth_variant_support_reverse_strand))
	filter_command+=" --adr " + depth_variant_support_reverse_strand

print("</br>Executed filter_command: </br></br>")
print(filter_command + "</br></br>")
print(compare_common_command + "</br></br>")
print(compare_unique_command + "</br></br>")

# ok, first lets break down the multisample vcf file to individual samples

def filter_multisample(namearray):
	array=[]
	for name in namearray:
		if name.startswith("multiplesamples_"):
			array.append(name)
	return array

def add_extension(data):
	text=[]
	for x in data:
		text.append(x + ".vcf.gz")

	return text

def read_vcf_get_header(vcf):
	handle = open(vcf)
	for line in handle:
		if line.startswith("#CHROM"):
			break
	handle.close()
	return line

def get_number_of_samples_from_vcf(vcf):
	handle=open(vcf)
	for line in handle:
		if line.startswith("#CHROM"):
			break
	handle.close()
	return line.strip().split("\t")[9:]

#out=open("output.log", 'w')
multiplesamples_keys=filter_multisample(form.keys())
#out.write(" ".join(multiplesamples_keys) + "\n")
for filename in input_vcfs:
	filename = dir_upload + filename
	samples=get_number_of_samples_from_vcf(filename)
	if len(samples) > 1:   # header has 9 columns + n number of samples
		# this is multiple sample vcf


		multisampleid="multiplesamples_" + "_".join(samples)
		print("<p>multiplesampleid - " + multisampleid + "</p>")
		selected_samples = form.getvalue(multisampleid)
		question = "name_question_" + "_".join(samples)
		print("name_question - " + question  + "</p>")

		samples_to_merge=[]
		samples_to_delete=[]
		if form.getvalue(multisampleid):
			if isinstance(selected_samples, list) and len(selected_samples) >1:
				print("<p>Selected sample - " + " ".join(selected_samples) + "</p>")
				for sample in selected_samples:

					print("<p>Splitting sample - " + sample + "</p>")
					cmd="perl -I " + rootdir + "lib " + rootdir + "vcftoolScripts/vcf-subset --columns " + sample + " " + filename + " > " + dir_process + sample + ".vcf"
					#out.write(cmd + "\n")
					os.system(cmd)
					cmd=rootdir + "otherscripts/bgzip " + dir_process + sample + ".vcf; " + rootdir + "otherscripts/tabix -f " + dir_process + sample + ".vcf.gz"
					#out.write(cmd + "\n")
					print("<p>" + cmd + "</p>")
					os.system(cmd)
					samples_to_merge.append(dir_process + sample)
					samples_to_delete.append(dir_process + sample + ".vcf*")

				if form.getvalue(question):
					# user has checked to merge the selected samples as one
					print("<p>Question - " + question  + " On/off - " + form.getvalue(question) + "</p>")
					print("<p>Now merging the above processed samples - " + ",".join(selected_samples) + "</p>")
					cmd = "perl -I " + rootdir + "lib " + rootdir + "vcftoolScripts/vcf-merge -d " + " ".join(add_extension(samples_to_merge)) + " > " + dir_process + "_".join(selected_samples) + ".vcf; " + rootdir + "otherscripts/bgzip " + dir_process + "_".join(selected_samples) + ".vcf;" + rootdir + "otherscripts/tabix " + dir_process + "_".join(selected_samples) + ".vcf.gz;"
					#also remove the samples after merging
					cmd+=" cd " + dir_process + "; rm " + " ".join(samples_to_delete)
					print("<p>" + cmd + "</p>")
					os.system(cmd)

				else:
					pass

			else:
				# one one sample selected
				print("<p>One sample selected from the multisampled file</p>")
				print("<p>Splitting out sample - " + selected_samples + "</p>")
				cmd="perl -I " + rootdir + "lib " + rootdir + "vcftoolScripts/vcf-subset --columns " + selected_samples + " " + filename + " > " + dir_process + selected_samples + ".vcf"
				os.system(cmd)
				print("</br>")
				print("<p>Processing sample - " + selected_samples + "</p>")
				cmd=rootdir + "otherscripts/bgzip " + dir_process + selected_samples + ".vcf; " + rootdir + "otherscripts/tabix -f " + dir_process + selected_samples + ".vcf.gz"
				os.system(cmd)

		#out.write(multisampleid + "\n" + question  + "\n")
	else:
		#only one sample
		#out.write("only one sample here\n")
		print("<p>Processing sample - " + samples[0] + "</p>")
		cmd=rootdir + "otherscripts/bgzip " + dir_upload + samples[0] + ".vcf; mv " + dir_upload + samples[0] + ".vcf.gz " + dir_process + "; " + rootdir + "otherscripts/tabix " + dir_process + samples[0] + ".vcf.gz"
		#out.write(cmd + "\n")
		print("<p>" + cmd + "</p>")
		os.system(cmd)

print("</body>")
print("</html>")
