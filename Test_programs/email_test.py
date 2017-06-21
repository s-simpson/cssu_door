

#https://support.google.com/accounts/answer/6010255?hl=en

#change account for less secure apps for this to work, otherwise 2 step authentication needed.

#https://myhydropi.com/send-email-with-a-raspberry-pi-and-python


import smtplib

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login("<sender@gmail.com>", "<enter-the-actual-password_here>")
msg = "This is a simple email test from the raspberry pi"
server.sendmail ("sender@gmail.com", "recipient_email@gmail.com", msg)
server.quit()

