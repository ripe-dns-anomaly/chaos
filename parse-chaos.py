import base64
import json
from pprint import pprint
import os
import sys

if (len(sys.argv) != 3):
	print "ERROR: What file to parse (arg 1) and where to write (arg 2)?"
	quit()

with open(sys.argv[1]) as json_data:
	data = json.load(json_data)
	json_data.close()

#print 'Reading from %s and writing to %s' % (sys.argv[1], sys.argv[2])

f = open(sys.argv[2], 'a+')

# Total of objects in the JSON file
pr = len(data)

#print 'TOTAL = %d' % pr

index = -1
c_hit = 0
c_err = 0

for res in data:
	index += 1
#	print data[index]

	if not res.get('error'):

		if data[index]['result'].get('answers'):
			c_hit += 1

			if isinstance(data[index]['result']['answers'][0]['RDATA'], list):
				f.write('%s %s %s\n' % (data[index]['prb_id'], data[index]['result']['answers'][0]['RDATA'][0], data[index]['result']['rt']))
			else:
				f.write('%s %s %s\n' % (data[index]['prb_id'], data[index]['result']['answers'][0]['RDATA'], data[index]['result']['rt']))

		else:
			c_err += 1
	else:
		c_err += 1

f.close()

print ' total CHAOS %d' % index
print ' total hits  %d' % c_hit
print ' total error %d' % c_err

