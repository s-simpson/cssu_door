#!/usr/bin/env python

######################################################################
# program tweety_pi_emailer.py by Stuart Simpson
# June 21, 2017
# 
# purpose:  This program emails and tweets incessantly about
#           The status of the door in the cssu office.
#           is the door open or is it closed?  
#           The tension is palpable and unbearable. 
#
#  NOW uses secure_google email
#   
# to run use python 2.7, raspian jessie 2017 04 10 version
# from command line:  python door_monitor.py
# 
# set to launch at startup
#   
#  see on_reboot.sh in the garage-door-controller directory
#  for more informaton.
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
#		             door_open_tweets.txt 		  
#  
#  
######################################################################

SEND_EMAIL = True 	       # flag to enable/disable sending emails
SEND_TWEET = True         # flag to enable/disable sending tweets

SEND_PUT_MESSAGE = False  # flag to enable/disable sending door status put message to a URL for maybe a webpage (untestested with a webpage)  
						   # message is {'cssu_door' : 'open'}  or {'cssu_door' : 'closed'}.
                           # need to add valid put destination url (put_message_url) in the passwords file (pswds.json) 
                           # fill in data with password_maker.py and run "python password_maker.py" to update pswds.json file. 
import requests

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

import base64
import httplib2

from email.mime.text import MIMEText

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

import argparse
from oauth2client import tools

fromaddr = "" 		#gmail address that we are sending the email from.  (stored in pwds.json) (see password_maker.py)
toaddr = ""  		#gamil address that we are sending the email to.  (right now we have set as the same adddress, see password_maker.py)

door_closed_tweet = "/home/pi/garage-door-controller/tweety_pi_emailer/door_closed_tweets.txt"  #text file filled with random door closed tweet messages
door_open_tweet = "/home/pi/garage-door-controller/tweety_pi_emailer/door_open_tweets.txt"      #text file filled with random door open tweet messages
passwords_file = "/home/pi/garage-door-controller/tweety_pi_emailer/pwds.json"			        #json file created to store config/password information

#get the data from the passwords file.

try:
	data = json.load(open(passwords_file), object_pairs_hook=OrderedDict)
except IOError as e:
	print "could not read file: ", passwords_file	
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

#all keys are stored in pwds.json file, edit by changing and running 
#password_maker.py (python password_maker.py) in this directory

#IMPORTANT:  THESE KEYS NEED TO BE KEPT SECRET!!!!  
#don't upload to github in a readable format

#data stored in 'pwds.json'
try:
	#these 4 items are twitter security keys
	API_KEY = data['api_key']						 
	API_KEY_SECRET = data['api_key_secret']
	ACCESS_TOKEN = data['access_token']
	ACCESS_TOKEN_SECRET = data['access_token_secret']
	
	#sender address
	fromaddr = data['gmail_account']                
	
	#recipents address(es)
	toaddr = data['gmail_recipients']
	
	#client secret file for gmail
	client_secret_file = data['gmail_client_secret_file']
	
	#url for webhook
	put_message_url = data['put_message_url']

except KeyError as e:
	print "One of the keys in the pwds.json file is missing."
	print "make sure all required keys are added to password_maker.py." 
	print "run 'python password_maker.py' from the command line"
	
	
#alladdr = toaddr.split(",") #more than one email address? separate them for later
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


def sendOurMail(fromaddr, toaddr,subject_line, message_body, client_secret_file):
	
#########################################################################################################
# purpose:  this function sends an email out via a gmail address without compromising security settings.
#          
#https://stackoverflow.com/questions/25944883/how-to-send-an-email-through-gmail-without-enabling-insecure-access
#
#  setting up the inital gmail settings details are here.  Takes some fiddling
#
#several modificatons to original code, change body line as per comment
#change from flow to run_flow
#
#this is working now! Yay the modifications worked 
#you have to do an email confirmation for inital setup, then is automatic seems to work so far.
#
#  tested initially in the email_secure_test.py program in the Test_programs folder.
#         
#
#          calling:  sendOurMail (fromaddr, toaddr, email_subject_line, message_body, client_secret_file)
#########################################################################################################

	# Path to the client_secret.json file downloaded from the Developer Console (ignore path put in same local dir as this file)
	CLIENT_SECRET_FILE = client_secret_file
	
	# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
	OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'
	
	# Location of the credentials storage file
	STORAGE = Storage('gmail.storage')
	
	# Start the OAuth flow to retrieve credentials
	flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
	http = httplib2.Http()
	
	# Try to retrieve credentials from storage or run the flow to generate them
	credentials = STORAGE.get()
	if credentials is None or credentials.invalid:
	  parser = argparse.ArgumentParser(parents=[tools.argparser])
	  flags = parser.parse_args()	
	  credentials = tools.run_flow(flow, STORAGE, flags)
	
	# Authorize the httplib2.Http object with our credentials
	http = credentials.authorize(http)
	
	# Build the Gmail service from discovery
	gmail_service = build('gmail', 'v1', http=http)
	
	# create a message to send
	message = MIMEText(message_body)
	message['to'] = toaddr
	message['from'] = fromaddr
	message['subject'] = subject_line
	body = {'raw': base64.b64encode(message.as_string()).replace('+','-').replace('/','_')}
	
	# send the email message
	try:
	  message = (gmail_service.users().messages().send(userId="me", body=body).execute())
	  print('Message Id: %s' % message['id'])
	  print(message)
	except Exception as error:
	  print('An error occurred: %s' % error)
	  
######################################################################
	  
def start_state():
	"""
	purpose:  This is the initial (unknown) state of the program.
	          It is not known whether the door is open or closed, so
	          we stay here and read for input.
	          
	          when we know whether the door is open or not we go to
	          the appropriate state function.
	"""	
	print "Starting Tweety_pi_emailer.py"
	while True:
		
		if( GPIO.input (BUBBLE_SWITCH_PIN) == CLOSED_DOOR):
			closed_door_state()
		
		time.sleep(0.1) #need slight delay to avoid double readings	
		
		if( GPIO.input (BUBBLE_SWITCH_PIN) == OPEN_DOOR):
			open_door_state()
		
		time.sleep(0.1) #need slight delay to avoid double readings
		
#######################################################################		  

def closed_door_state():
	
	"""
	purpose: when the door is in the closed state we send the closed
	door tweets, emails and put requests depending on whether
	SEND_TWEET, SEND_EMAIL, and SEND_PUT_MESSAGE are True or not.
	The program then waits for the state of the door to change to open
	
	If the door is now open we call (switch) to the open_door_state.
	
	"""
	
	ts = time.time()  #get timestamp of door state change
	print "DOOR IS CLOSED."
	time.sleep(0.1) #need slight delay to avoid double readings
	
	print "Sending door [CLOSED] tweet."
	rand_tweet = randomline (door_closed_tweet)
	rand_tweet = rand_tweet.rstrip('\r\n')
	rand_tweet = rand_tweet + " " + datetime.now().strftime("%H:%M:%S.%f")  #timestamp to avoid duplicate tweet error
	print rand_tweet
	
	if (SEND_TWEET):
		try:
			api.update_status(status=rand_tweet) #send tweet
		except TwythonError as e:
			print e.error_code
		
	#send email message
	if (SEND_EMAIL):
		print "Sending an email about the door being [CLOSED]."
		sendOurMail(fromaddr,toaddr, "CSSU Door is now CLOSED", rand_tweet, client_secret_file)
	
	#send put request for webhook
	if (SEND_PUT_MESSAGE):
		print "Sending http put message {'cssu_door' : 'closed'} to URL:  " + put_message_url
		try:
			r = requests.put(put_message_url, data = {'cssu_door' : 'closed'}) #not sure to use put or post here (r=request.post ...)
		except Exception as error:
			print("put request for door close failed")
			print('An error occurred: %s' % error)
	
	reading = GPIO.input (BUBBLE_SWITCH_PIN)   #wait until the state changes
	
	while ( reading == CLOSED_DOOR):
		time.sleep(0.1) #need slight delay to avoid double readings 
		reading = GPIO.input (BUBBLE_SWITCH_PIN)
	
	#reading = OPEN_DOOR so change states
	open_door_state()
		
#####################################################################################################################################

def open_door_state():
	
	"""
	purpose: when the door is in the open state we send the open
	door tweets, emails and put requests depending on whether
	SEND_TWEET, SEND_EMAIL, and SEND_PUT_MESSAGE are True or not.
	The program then waits for the state of the door to change to closed
	
	If the door is now closed we call (switch) to the closed_door_state.
	
	"""
	
	ts = time.time()  #get timestamp of door state change
	print "DOOR IS OPEN"
	time.sleep(0.1) #need slight delay to avoid double readings
	
	print "Sending door [OPEN] tweet."
	rand_tweet = randomline (door_open_tweet)
	rand_tweet = rand_tweet.rstrip('\r\n')
	rand_tweet = rand_tweet + " " + datetime.now().strftime("%H:%M:%S.%f")  #timestamp to avoid duplicate tweet error
	print rand_tweet
	
	if (SEND_TWEET):
		try:
			api.update_status(status=rand_tweet) #send tweet
		except TwythonError as e:
			print e.error_code
		
	#send email message
	if (SEND_EMAIL):
		print "Sending an email about the door being [OPEN]."
		sendOurMail(fromaddr,toaddr, "CSSU Door is now OPEN", rand_tweet, client_secret_file)
	
	#send put request for webhook
	if (SEND_PUT_MESSAGE):
		print "Sending http put message {'cssu_door' : 'open'} to URL:  " + put_message_url
		try:
			r = requests.put(put_message_url, data = {'cssu_door' : 'open'}) #not sure to use put or post here (r=request.post ...)
		except Exception as error:
			print("put request for door open failed")
			print('An error occurred: %s' % error)
	
	reading = GPIO.input (BUBBLE_SWITCH_PIN)   #wait until the state changes
	
	while ( reading == OPEN_DOOR):
		time.sleep(0.1) #need slight delay to avoid double readings 
		reading = GPIO.input (BUBBLE_SWITCH_PIN)
	
	#reading = CLOSED_DOOR change states
	closed_door_state()	

###############################################################
# Configure the GPIO pin  INIT FOR READ OF DOOR SENSOR

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUBBLE_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #with pull up no need for external resisitors

#################### main loop ################################

try:
	while True:
		start_state()
							 					
finally:
    print('Cleaning up GPIO')
    GPIO.cleanup()


