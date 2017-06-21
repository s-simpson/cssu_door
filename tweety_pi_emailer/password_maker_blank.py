#!/usr/bin/env python

import json
from collections import OrderedDict

######################################################################
"""
password_maker.py

Stuart Simpson June 19, 2017

small utilty program to create a json file named pwds.json
that is used by our programs to read in the data
for the various passwords if the passwords change, fill in the
updates here and run

this program

to run: command line  python password_maker.py

"""
#######################################################################

###################################################################
#need info from our twitter account in order for authorization.
#raspberry pi twitterbot FYI
#www.instructables.com/id/Raspberry-Pi-Twitterbot/
#www.makeuseof.com/tag/how-to-build-a -raspberry-pi-twitter-bot/
####################################################################

#api_key, api_key_secret, access_token, and access_token_secret
#are twitter secret passwords

#gmail_account is the gmail account that we are emailing from
#gmail_password is the gmail account's (sending account) password.

#gmail_recipients are who we are sending the emails to:  (can have more than one, separated with a comma)
#ie  'gmail_recipients' : 'cssudoor.com, secondemail.com'

#could use the email account as a trigger for othe functions
#if this then that?

#also can set up the messages to goto facebook if you want
#there is a bot on the twitter page

#select CSSu logo left of the tweet button
#apps
#there will be 2 apps there:

#facebook connect (post tweets to your facebook profile or page

#the other app is cssu_door_status which is how the door_emailer.py communicates with
#twitter. (door_emailer.py sends twitter tweets and gmail emails) 


passwords = {
	'api_key' : '',
	'api_key_secret' : '',
	'access_token'   : '',
	'access_token_secret' : '',
	'gmail_password' : '',
	'gmail_account' : '',
	'gmail_recipients' : ''
}


with open ('pwds.json', 'w') as f:
	json.dump(passwords, f)
