#!/usr/bin/python3

import sys
# Import modules for CGI handling
import cgi, cgitb

# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields
variable = ""
value = ""
r = ""
for key in form.keys():
        variable = str(key)
        value = str(form.getvalue(variable))
        r += "<p>"+ variable +", "+ value +"</p>\n"

fields = "<p>"+ str(r) +"</p>"
print(fields)
