#!/usr/bin/env python

import smtplib
import email

"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
"""

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromaddr = "from_email@gmail.com"
toaddr = "to_email@gmail.com"  #can have multiple addrs, separate with a comma

alladdr = toaddr.split(",") 

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "CSSU Door Status"
f = open('body.txt')
body = f.read()
msg.attach(MIMEText(body,'plain'))

#attachment file

#filename = "AttachmentFileWithExt"
#attachment = open("FullPathToFile", "rb")

#part = MIMEBase('application', 'octet-stream')
#part.set_payload((attachment).read())
#encoders.encode_base64(part)
#part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
#msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(fromaddr, "<ENTER_YOUR_ACTUAL_PASSWORD_FOR_THE_SENDERACCT>")
text = msg.as_string()
server.sendmail(fromaddr, alladdr, text)
server.quit()
