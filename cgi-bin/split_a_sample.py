#!/user/bin/env python3

#get sample name to split


# Import modules for CGI handling
import cgi, cgitb

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields

samplename = form.getvalue('samplename')

scriptname="split_vcf_samples.py"

filter_command="python3 " + scriptname

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>CGI Program</title>")
print("</head>")
print("<body>")
print("<h2>Data provided are below</h2>")

print("You have input following files:  </br>  </br>")
if samplename:
	print("Sample name to split: %s </br> </br>") % samplename


print("</body>")
print("</html>")
