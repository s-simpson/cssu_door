#!/usr/bin/env python

"""
Stuart Simpson June 20, 2017

password_reader.py

test program to read in a json file into a dictionary

to run:  (command line)  python password_reader.py


"""

import json
from collections import OrderedDict

data = json.load(open('pwds.json'), object_pairs_hook=OrderedDict)
print json.dumps(data, indent=4)


for k, v in data.items():
	print k,v
	

#print data['api_key']
