#!/usr/bin/env python

######################################################################
# program door_monitor.py by Stuart Simpson
# May 31 2017
# 
# purpose to test the state of the door leads
# when the program is first started it prints the state of the door
# when the state of the door changes, the program prints the new state
#
#
# to run use python 2.7, raspian jessie 2017 04 10 version
# from command line:  python door_monitor.py
#
######################################################################

import random
import os
import sys
from twython import Twython

#for twython need to "sudo pip install requests requests_oauthlib" to install correctly

import time
import RPi.GPIO as GPIO
import urllib2

door_closed_tweet = "door_closed_tweets.txt"  #text file filled with random door closed tweet messages
door_open_tweet = "door_open_tweets.txt"      #text file filled with random door open tweet messages

#need info from our twitter account in order for authorization.

API_KEY = ''
API_KEY_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

api = Twython (API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

BUBBLE_SWITCH_PIN = 23   # pin for status of door
OPEN_DOOR = 1    #when pin reads 1 on this switch the door is open
CLOSED_DOOR = 0  #when pin reads 0 on this switch the door is closed

#############################################################
#using pin BCM23 (pin16) for switch, and pin 9 for ground.
#see https://pinout.xyz/pinout/pin13_gpio27#
#for diagram of raspberry pi model 3 pins
#############################################################

MAX_TIME = 2 # time in seconds that a door must remain open or closed
             # before we send a tweet, don't want to send false tweets.

tweet_sent = True # assume that we've tweeted about the door by default

ts = 0 # timestamp

door_state = False   	 #current state of door, False because no door sensor read yet.  (Door could be open or closed when pi boots/program starts)
old_door_state = False   # ditto, also there was no old_door state if there was no initial door state yet.
                          # only want an event to happen when the door changes states.  

rand_tweet ="" #random tweet message


def randomline(filename):
	
###########################################################################################
# purpose:  returns a random line from a text file
# https://stackoverflow.com/questions/14924721/how-to-choose-a-random-line-from-a-text-file
#	
# assumes that the file exists and can be read.  no error checking
###########################################################################################

	
	fh = open(filename, "r")
	lineNum = 0
	it =""
	
	while True:
		aLine = fh.readline()
		lineNum = lineNum + 1
		if aLine != "":                        #stop reading at the end of the file.
			if random.uniform(0,lineNum) <1:
				it = aLine
		else:
			break
	nmsg = it
	return nmsg


# Configure the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUBBLE_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #with pull up no need for external resisitors


try:  
    while True:
         if ( GPIO.input(BUBBLE_SWITCH_PIN) == CLOSED_DOOR ):
              if (door_state == False or door_state == 'open'):
				  door_state = 'closed'
              
              if (old_door_state != door_state):
				  tweet_sent = False
				  ts = time.time()
				  print "door closed."
				  old_door_state = door_state
				  time.sleep(0.1) #need slight delay to avoid double readings
				
              if (old_door_state == door_state):
				  #print "they are the same"
				  if (time.time() - ts > MAX_TIME and tweet_sent == False):
					  print "sending door closed tweet"
					  rand_tweet = randomline (door_closed_tweet)
					  print rand_tweet
					  #api.update_status(status=rand_tweet) #to actually send tweet uncomment this line
					  tweet_sent = True 
				     
         elif ( GPIO.input(BUBBLE_SWITCH_PIN) == OPEN_DOOR ):
			 if (door_state == False or door_state == 'closed'):
				 door_state = 'open'
			  
			 if (old_door_state != door_state):
				 print "door open."
				 tweet_sent = False
				 ts=time.time()
				 old_door_state = door_state
				 time.sleep(0.1) #need slight delay to avoid double readings
				 
			 if (old_door_state == door_state):
				 #print "they are the same"
				 if (time.time() - ts > MAX_TIME and tweet_sent == False):
					 print "sending door opened tweet"
					 rand_tweet = randomline (door_open_tweet)
					 print rand_tweet
					 #api.update_status(status=rand_tweet) #to actually send tweet uncomment this line
					 tweet_sent = True 
											
finally:
    print('Cleaning up GPIO')
    GPIO.cleanup()
