#!/usr/bin/env python

#############################################################
# test program to read and print a random line from a text file
# program also indicates if the line is over 140 characters
# which is the maximum length of a tweet.   
#############################################################

readFilename = "door_open_tweets.txt"
#readFilename = "door_closed_tweets.txt"

MaxLen = 140 #tweets max 140 characters

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
		
	line = randomline(readFilename)
	if (len(line) > MaxLen):
		print line
		print len(line)  #line is over 140 characters oops need to shorten it I guess.  
	else:
		print line

