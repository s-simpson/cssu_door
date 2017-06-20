#!/usr/bin/env python

######################################################################
# program door_monitor.py by Stuart Simpson
# May 31 2017
# 
# purpose to test the state of the door leads
# when the program is first started it prints the state of the door
# when the state of the door changes, the program prints the new state
# it sends the information out to twitter account in the form
# of a randomly selected message. 
#
# to run use python 2.7, raspian jessie 2017 04 10 version
# from command line:  python door_monitor.py
# 
# to set to launch at startup
# sudo nano /etc/rc.local
# add line to /etc/rc.local above the call to exit 0:
# (cd ~pi/garage-door-controller; python door_monitor.py) &
#
#  ********** IMPORTANT NOTE *********************************
#
#  Don't upload API KEY INFORMATION/ACCESS TOKEN INFO TO GITHUB 
#  IF IT CAN BE READ IN A PUBLIC MANNER as security will be compomised
#     
#  Dependencies:  all of the import libraries must be installed
#  
#  files needed:  pwds.json must be configured correctly
#				  (see password_maker.py)
#	              
#                 also need tweet data files:
#                    door_closed_tweets.txt
#				  	 door_open_tweets.txt 		  
#  
#  
######################################################################

import random
import os
import sys
from twython import Twython

#for twython need to "sudo pip install requests requests_oauthlib" to install correctly
#not sure why, but it should work ok now

import time
from datetime import datetime
import RPi.GPIO as GPIO
import urllib2

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

import json
from collections import OrderedDict

SEND_EMAIL = True 	#flag to enable/disable sending emails
SEND_TWEET = True   #flag to enable/disable sending tweets

fromaddr = "" 		#gmail address that we are sending the email from.  (stored in pwds.json) (password_maker.py)
toaddr = ""  		#can have multiple destination addrs, separate with a comma, email recipients (see pwds.json) (password_maker.py)
                    #right now the recipients and the sender are the same address.

door_closed_tweet = "/home/pi/garage-door-controller/door_closed_tweets.txt"  #text file filled with random door closed tweet messages
door_open_tweet = "/home/pi/garage-door-controller/door_open_tweets.txt"      #text file filled with random door open tweet messages
passwords_file = "/home/pi/garage-door-controller/pwds.json"				  #json file created to store config/password information

try:
	data = json.load(open(passwords_file), object_pairs_hook=OrderedDict)
except IOError as e:
	print "could not read file: ", filename	
	print "I/O error ({0}): {1}", format(e.errorno, e.strerror)
	sys.exit() 
except:  #handle other errors
	print "Unexpected error: ", sys.exc_info()[0]
	sys.exit()

#print json.dumps(data, indent=4)

###################################################################
#need info from our twitter account in order for authorization.

#raspberry pi twitterbot FYI
#www.instructables.com/id/Raspberry-Pi-Twitterbot/
#www.makeuseof.com/tag/how-to-build-a -raspberry-pi-twitter-bot/
####################################################################

#IMPORTANT:  THESE KEYS NEED TO BE KEPT SECRET!!!!  
#don't upload to github in a readable format

#data stored in 'pwds.json'

#these 4 items are twitter security keys
API_KEY = data['api_key']						 
API_KEY_SECRET = data['api_key_secret']
ACCESS_TOKEN = data['access_token']
ACCESS_TOKEN_SECRET = data['access_token_secret']

#sender password
gmail_password = data ['gmail_password']
#sender address
fromaddr = data['gmail_account']                
#recipents address(es)
toaddr = data['gmail_recipients']

alladdr = toaddr.split(",") #more than one email address? separate them for later
##################################################################

api = Twython (API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) #init api

BUBBLE_SWITCH_PIN = 23   # pin for status of door
OPEN_DOOR = 1    #when pin reads 1 on this switch the door is open
CLOSED_DOOR = 0  #when pin reads 0 on this switch the door is closed

#############################################################
#using pin BCM23 (pin16) for switch, and pin 9 for ground.
#see https://pinout.xyz/pinout/pin13_gpio27#
#for diagram of raspberry pi model 3 pins
#############################################################

MAX_TIME = 2 # delay time in seconds that a door must remain open or closed
             # before we send a tweet, don't want to send false tweets.

tweet_sent = True # assume that we've tweeted about the door by default

ts = 0 # timestamp

door_state = False   	 #current state of door, False initally because door sensor unread.  (Door could be open or closed when pi boots/program starts)
old_door_state = False   # ditto, also there was no old_door state if there was no initial door state yet.
                          # We only want an event to happen when the door changes states.  

rand_tweet ="" #random tweet message none selected yet, will fill in later.


def randomline(filename):
	
###########################################################################################
# purpose:  returns a random line from a text file
# https://stackoverflow.com/questions/14924721/how-to-choose-a-random-line-from-a-text-file
#	
# assumes that the file exists and can be read.  
# added error checking if file missing
###########################################################################################

	try:
		fh = open(filename, "r")
	except IOError as e:
		print "could not read file: ", filename	
		print "I/O error ({0}): {1}", format(e.errorno, e.strerror)
	except:  #handle other errors
		print "Unexpected error: ", sys.exc_info()[0]
		sys.exit()
        
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


def sendOurMail(fromaddr, toaddr, alladdr, subject_line, message_body, gmail_password):
	
#########################################################################################################
# purpose:  this function sends an email out via a gmail address
#          the gmail address must have a lower security setting to function
#          correctly.
#          
#          see https://myhydropi.com/send-email-with-a-raspberry-pi-and-python
#          for more information.
#         
#
#          calling:  sendOurMail (fromaddr, toaddr, alladdr, email_subject_line, message_body, gmail_password)
#########################################################################################################

	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject_line
	msg.attach(MIMEText(message_body,'plain'))
	server = smtplib.SMTP('smtp.gmail.com',587) #587 works with gmail, might not work with other emails
	server.starttls()
	server.login(fromaddr, gmail_password)
	text = msg.as_string()
	server.sendmail(fromaddr, alladdr, text)
	server.quit()

###############################################################
# Configure the GPIO pin  INIT FOR READ OF DOOR SENSOR

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUBBLE_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #with pull up no need for external resisitors

#################### main loop ################################

try:  
    while True:
         if ( GPIO.input(BUBBLE_SWITCH_PIN) == CLOSED_DOOR ):
              if (door_state == False or door_state == 'open'):
				  door_state = 'closed'
              
              if (old_door_state != door_state):
				  tweet_sent = False
				  ts = time.time()  #get timestamp of door state change
				  print "door closed."
				  old_door_state = door_state
				  time.sleep(0.1) #need slight delay to avoid double readings
				
              if (old_door_state == door_state):
				  #print "they are the same"
				  if (time.time() - ts > MAX_TIME and tweet_sent == False):
					  print "sending door closed tweet"
					  rand_tweet = randomline (door_closed_tweet)
					  rand_tweet = rand_tweet.rstrip('\r\n')
					  rand_tweet = rand_tweet + " " + datetime.now().strftime("%H:%M:%S.%f")
					  print rand_tweet
					  if (SEND_TWEET):
						  api.update_status(status=rand_tweet) #to actually send tweet uncomment this line
					  tweet_sent = True
					  
					  #send email message
					  if (SEND_EMAIL):
						  print "Sending an email about the door being closed."
						  sendOurMail(fromaddr,toaddr, alladdr, "CSSU Door is now CLOSED", rand_tweet, gmail_password)
					   
				     
         elif ( GPIO.input(BUBBLE_SWITCH_PIN) == OPEN_DOOR ):
			 if (door_state == False or door_state == 'closed'):
				 door_state = 'open'
			  
			 if (old_door_state != door_state):
				 print "door open."
				 tweet_sent = False
				 ts=time.time()  #get timestamp of door state change
				 old_door_state = door_state
				 time.sleep(0.1) #need slight delay to avoid double readings
				 
			 if (old_door_state == door_state):
				 #print "they are the same"
				 if (time.time() - ts > MAX_TIME and tweet_sent == False):
					 print "sending door opened tweet"
					 rand_tweet = randomline (door_open_tweet)
					 rand_tweet = rand_tweet.rstrip('\r\n')
					 rand_tweet = rand_tweet + " " + datetime.now().strftime("%H:%M:%S.%f")
					 print rand_tweet
					 if (SEND_TWEET):
						 api.update_status(status=rand_tweet) #to actually send tweet uncomment this line
					 tweet_sent = True 
					 
					 #send email message
					 if (SEND_EMAIL):
						 print "Sending an email about the door being open."
						 sendOurMail(fromaddr,toaddr, alladdr, "CSSU Door is now OPEN", rand_tweet, gmail_password)
					 						
finally:
    print('Cleaning up GPIO')
    GPIO.cleanup()
