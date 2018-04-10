#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
resistant_parent = form.getvalue('resistant_parent')
susceptible_parent  = form.getvalue('susceptible_parent')
resistant_parent_forward_reads = form.getvalue('resistant_parent_forward_reads')
resistant_parent_reverse_reads = form.getvalue('resistant_parent_reverse_reads')
susceptible_parent_forward_reads = form.getvalue('susceptible_parent_forward_reads')
susceptible_parent_reverse_reads = form.getvalue('susceptible_parent_reverse_reads')
bulk_susceptible_forward_reads = form.getvalue('bulk_susceptible_forward_reads')
bulk_susceptible_reverse_reads = form.getvalue('bulk_susceptible_reverse_reads')

resistant_mapped_sambam = form.getvalue('resistant_mapped_sambam')
susceptible_mapped_sambam = form.getvalue('susceptible_mapped_sambam')
resistant_sample_vcfs = form.getvalue('resistant_sample_vcfs')
susceptible_sample_vcfs = form.getvalue('susceptible_sample_vcfs')


print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Data provided are below</h2>"
if resistant_parent:
	print("rake commands :")
	if isinstance(resistant_parent, list):
		#print("Resistant parent reference files are </br>")
		for name in resistant_parent:
			print(name + "</br>")
	else:
		print( "Resistant reference sequence: %s </br>") % (resistant_parent)
if susceptible_parent:
	if isinstance(susceptible_parent, list):
		print("Susceptible parent reference files are </br>")
		for name in susceptible_parent:
			print(name + "</br>")
	else:
		print( "Susceptible reference sequence: %s </br>") % (susceptible_parent)
if resistant_parent_forward_reads and resistant_parent_reverse_reads:
	if isinstance(resistant_parent_forward_reads, list) and isinstance(resistant_parent_reverse_reads, list) and len(resistant_parent_forward_reads) == len(resistant_parent_reverse_reads):
		print("Resistant parents raw reads are </br>")
		for forward, reverse in zip(resistant_parent_forward_reads, resistant_parent_reverse_reads):
			print(forward + " " + reverse + "</br>")
			print("rake R1=" + forward + " R2=" + reverse + " reference=" + resistant_parent)
	else:
		print( "Resistant short read sequences: %s %s</br>") % (resistant_parent_forward_reads, resistant_parent_reverse_reads)
		print("rake R1=" + forward + " R2=" + reverse + " reference=" + resistant_parent)

if susceptible_parent_forward_reads and susceptible_parent_reverse_reads:
	if isinstance(susceptible_parent_forward_reads, list) and isinstance(susceptible_parent_reverse_reads) and len(susceptible_parent_forward_reads) == len(resistant_parent_reverse_reads):
		print("Susceptible parent raw reads are </br>")
		for forward, reverse in zip(susceptible_parent_forward_reads, susceptible_parent_reverse_reads):
			print(forward + " " + reverse + "</br>")
			print("rake R1=" + forward + " R2=" + reverse + " reference=" + susceptible_parent)
	else:
		print( "Susceptible short read sequence: %s %s</br>") % (susceptible_parent_forward_reads, susceptible_parent_reverse_reads)
		print("rake R1=%s R2=%s reference=%s </br>") % (susceptible_parent_forward_reads, susceptible_parent_reverse_reads, susceptible_parent)
if bulk_susceptible_forward_reads and bulk_susceptible_reverse_reads:
	if instance(bulk_susceptible_forward_reads, list) and instance(bulk_susceptible_reverse_reads) and len(bulk_susceptible_forward_reads) == len(bulk_susceptible_reverse_reads):
		print("bulk susceptible raw reads are ")
		for forward, reverse  in zip(bulk_susceptible_forward_reads, bulk_susceptible_reverse_reads):
			print(forward + " " + reverse + "</br>")
			print("rake R1=" + forward + " R2=" + reverse + " reference=" + susceptible_parent)
	else:
		print( "Bulk susceptible sequence reads: %s %s</br>") % (bulk_susceptible_forward_reads, bulk_susceptible_reverse_reads)
		print("rake R1=" + forward + " R2=" + reverse + " reference=" + susceptible_parent)



if susceptible_mapped_sambam:
	print( "Susceptible sample sambam :  %s </br> ") % (susceptible_mapped_sambam)
if resistant_mapped_sambam:
	print( "Resistant sample sambam : %s </br>") % (resistant_mapped_sambam)

if resistant_sample_vcfs:
	print("First VCF file:  %s") %s (resistant_sample_vcfs)

if susceptible_sample_vcfs:
	print("Second VCF file: %s") %s (susceptible_sample_vcfs)

print "</body>"
print "</html>"
