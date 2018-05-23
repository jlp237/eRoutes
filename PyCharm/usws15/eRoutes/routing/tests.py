from django.test import TestCase

# Create your tests here.

import cgi
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')