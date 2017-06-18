#!/usr/bin/env python


MaxLen = 140

import os
import random

def randomline(filename):
	fh = open(filename, "r")
	lineNum = 0
	it =""
	
	while True:
		aLine = fh.readline()
		lineNum = lineNum + 1
		if aLine != "":
			if random.uniform(0,lineNum) <1:
				it = aLine
		else:
			break
	nmsg = it
	return nmsg


while True:
	
	filename = "door_open_tweets.txt"	
	line = randomline(filename)
	if (len(line) > 140):
		print line
		print len(line)
	else:
		print line

