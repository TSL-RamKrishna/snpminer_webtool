#!/usr/local/bin/python

# Import modules for CGI handling
import cgi, cgitb

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields

resistant_sample_vcfs = form.getvalue('resistant_sample_vcfs')
susceptible_sample_vcfs = form.getvalue('susceptible_sample_vcfs')
reference_sequence = form.getvalue('reference_sequence')
input_vcfs = form.getvalue("input_vcfs")
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

pythonscript="filter_vcf.py"
command="python3 " + pythonscript

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Data provided are below</h2>"

print("You have input following files:  </br>  </br>")
if reference_sequence:
	print("Reference Sequence: %s </br> </br>") % reference_sequence

if input_vcfs:
	if isinstance(input_vcfs, list):
		print("Input VCFs : %s </br></br>") % " ".join(input_vcfs)
	else:
		print("Input VCFs : %s </br></br>") % input_vcfs

print("You have selected following parameters:  </br> </br>")


if reference_sequence:
	print("Reference sequence : %s") % reference_sequence
	command+=" --reference " + reference_sequence
if input_vcfs:

	if isinstance(input_vcfs, list):
		command+=" --input " + ",".join(input_vcfs)
	else:
		command+=" --input " + input_vcfs

if genotype:
	print('Gentotype : %s </br>') % (genotype)
	command+=" --gt " + str(genotype)
if variant_allele_freq:
	print("Minimum Variant allele frequency (FREQ): %s </br>") % (variant_allele_freq)
	command+=" --freq " + variant_allele_freq
if per_sample_depth:
	print("Minimum Average per-sample depth of bases with Phred score >= 15 (ADP): %s </br>") % (per_sample_depth)
	command+=" --adp " + per_sample_depth
if sample_called_reference:
	print("Minimum Number of samples called reference (wild-type) (WT): %s </br>") % (sample_called_reference)
	command+=" --wt " + sample_called_reference
if not_called:
	print("Minimum Number of samples not called (NC): %s </br>") % not_called
	command+=" --nc " + nc_called
if genotype_quality:
	print("Minimum Genotype Quality(GQ): %s </br>") % genotype_quality
	command+=" --gq " + genotype_quality
if raw_read_depth:
	print("Minimum Raw Read Depth as reported by SAMtools (SDP): %s </br>") % raw_read_depth
	command+=" --sdp " + raw_read_depth
if quality_read_depth:
	print("Minimum Quality Read Depth of bases with Phred score >= 15 (DP) : %s </br>") % quality_read_depth
	command+=" --dp " + quality_read_depth
if ref_support_read_depth:
	print("Minimum Depth of reference-supporting bases (reads1) (RD): %s  </br>") % ref_support_read_depth
	command+=" --rd " + ref_support_read_depth
if variant_read_depth:
	print("Minimum Depth of variant-supporting bases (reads2) (AD): %s  </br>") % variant_read_depth
	command+=" --ad " + variant_read_depth
if pvalue:
	print("P-value from Fisher's Exact Test (PVAL) less or equal to : %s </br>") % pvalue
	command+=" --pvalue " + pvalue
if avg_qual_ref_support_bases:
	print("Minimum Average quality of reference-supporting bases (qual1) (RBQ): %s </br>") % avg_qual_ref_support_bases
	command+=" --rbq " + avg_qual_ref_support_bases
if avg_qual_variant_support_bases:
	print("Minimum Average quality of variant-supporting bases (qual2) (ABQ):%s </br>") % avg_qual_variant_support_bases
	command+=" --abq " + avg_qual_variant_support_bases
if depth_ref_support_forward_strand:
	print("Minimum Depth of reference-supporting bases on forward strand (reads1plus) (RDF): %s </br>") % depth_ref_support_forward_strand
	command+=" --rdf " + depth_ref_support_forward_strand
if depth_ref_support_reverse_strand:
	print("Minimum Depth of reference-supporting bases on reverse strand (reads1minus) (RDR): %s </br>" ) % depth_ref_support_reverse_strand
	command+=" --rdr " + depth_ref_support_reverse_strand
if depth_variant_support_forward_strand:
	print("Minimum Depth of variant-supporting bases on forward strand (reads2plus) (ADF) : %s </br>") % depth_variant_support_forward_strand
	command+=" --adf " + depth_variant_support_forward_strand
if depth_variant_support_reverse_strand:
	print("Minimum Depth of variant-supporting bases on reverse strand (reads2minus) (ADR) : %s </br>") % depth_variant_support_reverse_strand
	command+=" --adr " + depth_variant_support_reverse_strand

print"</br>Executed Command: </br></br>"
print(command + "</br></br>")
print "</body>"
print "</html>"
