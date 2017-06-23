README FIRST FILE (general information and Configuration details)
#######################################################################################################

README FIRST CSSU DOOR PROJECT  
Stuart Simpson
June 22/2017

GITHUB

https://github.com/s-simpson/cssu_door

#######################################################################################################
Other documentation in README_CSSU_DOOR.txt, and modifications.txt.

====================================================================================================
CSSU DOOR SENSOR General Information:
====================================================================================================

There are 2 main programs:  controller.py and tweety_pi_emailer.py 

Both programs start automatically upon boot via the "/home/pi/garage-door-controller/on_reboot.sh"  
(They are likely running already, if you are reading this from the raspberry pi with the software already installed)

1)  controller.py

Location:  /home/pi/garage-door-controller/
Purpose:   displays a local webpage that shows the status of the CSSU DOOR.
            
           How to use:
 
           in a browser (on this machine enter):  http://127.0.0.1:8081  (bookmarked in Chromium) 
           then you should see a door status webpage. (closed/open)

	   to see from another machine (on the same network), you can enter the ip address:
           ie http://192.168.0.19:8081  (if this is the raspberry pi's ip address)
	   
	   to see this machine's ip address either use 'ifconfig' from the command line (you can use ssh) or
           simply hover over the wireless icon at the top right corner of the desktop. 

	   The ip address may (probably will) change depending upon the network/reboots etc, unless you can have a static ip
           or have some sort of registered web address/domain it will be hard to see for the outside world.
	   
           Also:  http://127.0.0.1:8081/upd? (or http://192,168.0.19:8081/?upd) (whatever the ip of the pi) returns the status of the door 
           
           (when door is open)
           {"timestamp": 1498183221, "update": [["right", "open", 1498183214.895251]]}
	               
           (when door is closed)
	   {"timestamp": 1498183465, "update": [["right", "closed", 1498183452.894614]]}



2)  tweety_pi_emailer.py

Location: /home/pi/garage-door-controller/tweety_pi_emailer/

Purpose:  sends random twitter messages when the door/opens or closes to https://twitter.com/cssu_door
          and can also send the twitter messages to a gmail account if so desired.

          The program can also send simple put (or be modified to send a post message instead if thats better) webmessageto a url
          not sure if we need to implement other options like post, get

          
=======================================================================================================
tweety_pi_emailer.py Initial Configuration:

Simple settings (see lines 39-41 of tweety_pi_emailer.py)

FLAGS set to True to enable function, set to False to disable (save and reboot OR kill relevant python process and rerun tweety_py_emailer.py)
-----------------------
Default Settings:

SEND_EMAIL = True 	  
SEND_TWEET = True        
SEND_PUT_MESSAGE = False
-----------------------

for other settings, passwords/email addresses/

enter relevant passwords/data into password_maker.py and run "python password_maker.py" to update pwds.json file.
to see what you need, probably a good idea to examine password_maker.py within this directory.

-------
TWITTER:
-------

To set up a twitter account, you first should set up a separate email account ( I used gmail, since This program uses gmail to send mail too.)
it will also need a cell number for confirmation, but you can remove the cell phone number afterwards.
In order for this program to work you will need 4 special permission keys from Twitter.

The access codes are called something like:  apikey, apikey_secret, access_code, and access_code_secret.  

for a basic tutorial and instructions see this URL: (STEP 2 to STEP 8)

http://www.instructables.com/id/Raspberry-Pi-Twitterbot/

enter all of the twitter secret keys (4 of them) into password_maker.py, save and run "python password_maker.py" to update pwds.json file

-----
GMAIL:
-----

SetUp Instructions based upon this original article found at:

https://stackoverflow.com/questions/25944883/how-to-send-an-email-through-gmail-without-enabling-insecure-access#2594920

NAVIGATING THE GOOGLE WEBSITE IS HALF THE BATTLE

No doubt, over time, this will change. Ultimately you need to download a client_secret.json file. 
You can only (probably) do this setting up stuff via a web browser:

1) You need a google account - either google apps or gmail. So, if you haven't got one, go get one.
   (if you already have a gmail account, you can get another, but be sure to be logged into the new one,sometimes it defaults to the old one)
2) Get yourself to the developers console (https://console.developers.google.com/)  look for gmail api on the right.
3) Create a new project, and wait 4 or 400 seconds for that to complete.
4) Navigate to API's and Auth -> Credentials
5) Under OAuth select Create New Client ID
6) Choose Installed Application as the application type and Other
7) You should now have a button Download JSON. Do that. It's your client_secret.json—the passwords so to speak

8) Save/copy the client secret json file to the same directory as the tweety_pi_emailer.py program
9) put the new client secret json filename into password_maker.py, save and run "python password_maker.py to update pwds.json file.

BUT WAIT THAT'S NOT ALL

You have to give your application a "Product Name" to avoid some odd errors. (see how much I suffered to give you this ;-)

1) Navigate to API's & auth -> Consent Screen
2) Choose your email
3) Enter a PRODUCT NAME. It doesn't matter what it is. "Foobar" will do fine.
4) Save

NEWSFLASH! WHOA. NOW THERE'S EVEN MORE!

Navigate to API's & auth -> APIs -> Gmail API
Click the button Enable API
Yay. Now we can update the emailing script.

Python 2  (which is what we are using ~2.7)

You need to run the script interactively the first time. It will open a web browser on your machine and you'll grant permissions (hit a button). 
This exercise will save a file to your computer gmail.storage which contains a reusable token.

[I had no luck transferring the token to a machine which has no graphical browser functionality—returns an HTTPError. 
I tried to get through it via the lynx graphical browser. That also failed because google have set the final "accept" button to "disabled"!? 
I'll raise another question to jump this hurdle (more grumbling)]

First you need some libraries: 

pip install --upgrade google-api-python-client  (done)
pip install --upgrade python-gflags             (done) 

you need to change the email to and email from addresses (password_maker.py again)
make sure you have the client_token.json file whereever the Storage instructions expect it (in the folder /home/pi/garage-door-controller/tweety_pi_emailer/)
the directory needs to be writable so it can save the gmail.storage file

-------------------
Webhook PUT message
-------------------

1) in tweety_pi_emailer.py file ensure that (line42) SEND_PUT_MESSAGE = False is changed to SEND_PUT_MESSAGE = True. save the file 

2) Ensure that the webhook (put message) URL is entered into the password_maker.py script, run "python password_maker.py" from the command line.
This ensures that the pwds.json file is up to date.

Step 3)  kill or the python process and restart tweety_pi_emailer.py or save everything and reboot.  (process starts automatically)


open or closed messages

relevant program lines:(line 311 and 356) which are:

r = requests.put(put_message_url, data = {'cssu_door' : 'open'})
r = requests.put(put_message_url, data = {'cssu_door' : 'closed'})



