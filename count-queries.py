import base64
import json
from pprint import pprint
import os
import sys

if (len(sys.argv) != 2):
	print "ERROR: What file to parse (arg 1)?"
	quit()

with open(sys.argv[1]) as json_data:
	data = json.load(json_data)
	json_data.close()

# Total of objects in the JSON file
pr = len(data)

index = -1

for res in data:
	index += 1

print '%d' % index

