#!/usr/bin/python3

import sys, os
from subprocess import Popen, PIPE
import shutil
# Import modules for CGI handling
import cgitb
import cgi
import shutil

#dir_upload=os.path.dirname(sys.argv[0]) + "/../uploads/"
dir_upload="/home/shrestha/Sites/uploads/"

# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields

message="<p>"

if 'ramfiles' in form:
	filefield = form['ramfiles']
	if not isinstance(filefield, list):
		filefield = [filefield]

	for fileitem in filefield:
		if fileitem.filename:
			fn = os.path.basename(fileitem.filename)
		# save file
		with open(dir_upload + fn, 'wb') as fout:
			while True:
				chunk=fileitem.file.read(10000)
				if not chunk:
					break
				fout.write(chunk)

		message+=fn + " uploaded "
	message+="File upload completed "

else:
	message+="Files not found in form"

message+="</p>"
cgitb.enable()

print("""Content-type: text/html\n
<html>
<head>
<title>Multiple file upload test</title>
</head>
<body>
<h2>Files upload</h2>
%s
</body>
</html>
""" % (message) )
