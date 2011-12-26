#!/usr/bin/python
#required header that tells the browser how to render the text.

import cgi
import json
form = cgi.FieldStorage()
print "Content-Type: text/plain\n\n"

# Print a simple message to the display window.
#print "Args:"
#print form
print "response from python"
