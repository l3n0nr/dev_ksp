#!/usr/bin/env python
#
# REFERENCE: http://open-notify.org/Open-Notify-API/ISS-Location-Now/
#
import urllib2
import json

req = urllib2.Request("http://api.open-notify.org/iss-now.json")
response = urllib2.urlopen(req)

obj = json.loads(response.read())

longitude = obj['iss_position']['longitude']
latitude = obj['iss_position']['latitude']

print "Longitude: " + longitude
print "Latitude: "  + latitude 