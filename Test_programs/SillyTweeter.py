#!/usr/bin/env python

import sys
from twython import Twython
import os

cmd = '/opt/vc/bin/vcgencmd measure_temp'
line = os.popen(cmd).readline().strip()
temp = line.split('=')[1].split("'")[0]


#to run:  (command line)  python SillyTweeter.py 'twitter message from my raspberry pi'

###################################################################
#need info from our twitter account in order for authorization.

#raspberry pi twitterbot FYI
#www.instructables.com/id/Raspberry-Pi-Twitterbot/
#www.makeuseof.com/tag/how-to-build-a -raspberry-pi-twitter-bot/

#includes article on tweeting webcam pics if addition needed.

API_KEY = ''
API_KEY_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

##################################################################

api = Twython (API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) #init api

api.update_status(status=sys.argv[1])

api.update_status(status='My current CPU temperature is '+temp+' degrees C.')
