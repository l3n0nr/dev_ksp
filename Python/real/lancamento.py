#!/usr/bin/env python

import json, requests, os

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

response = requests.get("https://launchlibrary.net/1.2/launch?next=5")
todos = json.loads(response.text)

launches=todos["launches", "net"]
# net=todos[".net"]
# net=todos["launches"]

# print (launches)						# funcionando
print (launches)

# print todos
# print (todos["launches"])				# funcionando
# print todos["net{}"]
# print todos["launches"(net)]

## EXAMPLE
	# {u'net': u'October 20, 2018 01:45:28 UTC', 
	# u'tbddate': 0, 
	# u'id': 1073, 
	# u'tbdtime': 0, 
	# u'name': u'Ariane 5 ECA | BepiColombo'}, 