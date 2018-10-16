#!/usr/bin/env python

import json, requests, os

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

response = requests.get("https://launchlibrary.net/1.2/launch?next=5")
todos = json.loads(response.text)

# print todos
# print todos["launches"]		# funcionando
# print todos['launches{net}']
print todos["launches",{u'net'}]
# obj = {u"answer": [42.2], u"abs": 42}