#https://stackoverflow.com/questions/25944883/how-to-send-an-email-through-gmail-without-enabling-insecure-access

#several modificatons to original code, change body line as per comment
#change from flow to run_flow

#this is working now! Yay the modifications worked 
#you have to do an email confirmation 

import base64
import httplib2

from email.mime.text import MIMEText

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

import argparse
from oauth2client import tools

# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret_557759970213-0bo4unsl624nq8i44bm0hu91nhs3f5kg.apps.googleusercontent.com.json'

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
message = MIMEText("Message goes here.")
message['to'] = "cssudoor@gmail.com"
message['from'] = "cssudoor@gmail.com"
message['subject'] = "testing secure email"
body = {'raw': base64.b64encode(message.as_string()).replace('+','-').replace('/','_')}

# send it
try:
  message = (gmail_service.users().messages().send(userId="me", body=body).execute())
  print('Message Id: %s' % message['id'])
  print(message)
except Exception as error:
  print('An error occurred: %s' % error)
