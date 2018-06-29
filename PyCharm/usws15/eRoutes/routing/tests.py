from django.test import TestCase

# Create your tests here.

import cgi
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')


#todo
#round top speed in database
#Berlin Rom error (list index out of range) [x]
#station provider bug

#charging_stations muss mindestens 3 punkte zurück geben: laden im umkreis des zielpunktes