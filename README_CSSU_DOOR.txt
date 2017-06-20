
#######################################################################################################

README CSSU DOOR PROJECT  (initially from garage-door-controller) Documentation on important files.

Stuart Simpson
June 19/2017

GITHUB

https://github.com/s-simpson/cssu_door

#######################################################################################################

For door wiring information see door_monitor.py for more details in the documentation.

#############################################################
#using pin BCM23 (pin16) for switch, and pin 9 for ground.
#see https://pinout.xyz/pinout/pin13_gpio27#
#for diagram of raspberry pi model 3 pins
#############################################################


Files:
========================================================================================================
test_door.py

prints out the status of the door (open or closed) used to test operation of the door

run:  (from command line)  python test_door.py
========================================================================================================
door_monitor.py  (PURPOSE TO SEND TWEETS)  SEE door_emailer.py which also sends tweets.  

only run door_monitor.py or door_emailer.py, not both as you will get duplicate tweets.

prints out the status of the door (open or closed and sends tweets to the twitter account
https://twitter.com/cssu_door

randomly selects from tweets located in 'door_open_tweets.txt' or 'door_closed_tweets.txt'
depending on whether it is open or closed.  

The tweets are simple text messages that are of length <=140 characters followed by a carriage return

PROGRAM CAN BE SET TO AUTORUN ON THE PI

to run (from command line/terminal) python door_monitor.py
set to autorun on bootup in /etc/rc.local

(cd ~pi/garage-door-controller; python door_monitor.py) &

just before exit 0

sudo nano /etc/rc.local to edit this file (file protected permissions.)

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
reference websites:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
for background information
raspberry pi twitterbot FYI

www.instructables.com/id/Raspberry-Pi-Twitterbot/
www.makeuseof.com/tag/how-to-build-a -raspberry-pi-twitter-bot/

cssu_door_status application (used by test_door.py)

************************************************************************
https://apps.twitter.com/app/13942613   

https://twitter.com/cssu_door
************************************************************************

OPTIONS FOR EXPANSION:  FACEBOOK

There is an option also that I haven't tried yet but it seems that
the twitter website has an option to resend the tweets to facebook if 
that is desired

profiles and settings (icon next to tweet) upper right of webpage
select Apps, there is a prewritten facebook connect APP which should be
easy to setup if desired.


========================================================================================================
controller.py

This program generates a webpage that shows an icon of a door open/closed depending upon the status of
the door

to see the webpage on the pi run chromium browser (globe icon upper left)
(from local host)

http://127.0.0.1:8081/

if you want to see from another computer, you need to figure out the local ip address
this is how to do it.  (you can ssh into the pi, or hook it up to a monitor)

from command line:  ifconfig

pi@raspberrypi:~/garage-door-controller $ ifconfig
eth0      Link encap:Ethernet  HWaddr b8:27:eb:cf:ff:67  
          inet6 addr: fe80::2c:a9e1:7899:1add/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:460 errors:0 dropped:0 overruns:0 frame:0
          TX packets:460 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:58504 (57.1 KiB)  TX bytes:58504 (57.1 KiB)

wlan0     Link encap:Ethernet  HWaddr b8:27:eb:9a:aa:32  
          inet addr:192.168.0.12  Bcast:192.168.0.255  Mask:255.255.255.0
          inet6 addr: fd00:fc:8db8:67a2:5cbf:ac94:1da:ceeb/64 Scope:Global
          inet6 addr: 2607:fea8:205f:fbf5:bb7f:72bf:a5e0:5aa8/64 Scope:Global
          inet6 addr: fe80::ba27:ebff:fe9a:aa32/64 Scope:Link
          inet6 addr: 2607:fea8:205f:fbf5::3/128 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:104813 errors:0 dropped:1 overruns:0 frame:0
          TX packets:5913 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:19382630 (18.4 MiB)  TX bytes:707263 (690.6 KiB)

ip address in this case is 192.168.0.12 so we can access it by entering in Chromium

http://192.168.0.12:8081

if we are worrying about uptime changes to the ip address, this information might help

https://webmasters.stackexchange.com/questions/27589/how-can-i-host-a-website-on-a-dynamically-assigned-ip-address#27592

it is useful to check and see if everything is working ok.

 **** this program is set to autorun upon bootup

(cd ~pi/garage-door-controller; python controller.py) &

just before exit 0

sudo nano /etc/rc.local to edit this file

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
REFERENCE WEBSITES
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
https://github.com/s-simpson/cssu_door

https://github.com/andrewshilliday

(original garage-door-controller project)
========================================================================================================

read_file.py

test program to read a text file and print a random line from that file

========================================================================================================
SillyTweeter.py

test program that demonstrates how to send a tweet in python with Twython

========================================================================================================
door_emailer.py

makes use of password_maker.py for configuration of the pwds.json passwords file.
also depends upon the two tweet files:  door_open_tweets.txt, and door_closed_tweets.txt.

no error checking is done if the files are missing or incomplete, expect the program to not work ok.

this program sends tweets just like door monitor.py and also sends emails to the given email addresses
of the tweets.  Currently the program simply sends emails to the cssudoor@gmail.com website from
the cssudoor@gmail.com website.  addtional recipients could be added.

If you have door emailer running, there is no need to have door monitor also running, as they both send tweets
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
references website:

https://myhydropi.com/send-email-with-a-raspberry-pi-and-python
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
========================================================================================================

password_maker.py

program that generates the config data file for door_emailer.py and door_monitor.py

It must be ran and filled in correctly for these 2 programs to function

creates the pwds.json data file

to run:  (cmd line)  python password_maker.py

========================================================================================================
password_reader.py

utility program used to verify that the pwds.json file is working/written ok.


to run  (cmd line)  python password_reader.py
========================================================================================================
email_test.py and email_test2.py

two test programs for sending emails with the gmail account.
