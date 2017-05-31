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



import time
import RPi.GPIO as GPIO
import urllib2


BUBBLE_SWITCH_PIN = 23   # pin for status of door
OPEN_DOOR = 1    #when pin reads 1 on this switch the door is open
CLOSED_DOOR = 0  #when pin reads 0 on this switch the door is closed

#############################################################
#using pin BCM23 (pin16) for switch, and pin 9 for ground.
#see https://pinout.xyz/pinout/pin13_gpio27#
#for diagram of raspberry pi model 3 pins
#############################################################

EVENT = 'door_opens'
BASE_URL = 'https://maker.ifttt.com/trigger/'
KEY = 'cyR3vPNF32W4NZB9cd'

EVENT1 = 'door_closes'


door_state = False   	 # current state of door, False because no door sensor read yet.  (Door could be open or closed when pi boots/program starts)
old_door_state = False  # ditto, also there was no old_door state if there was no initial door state yet.
                         # only want an event to happen when the door changes states.  

# Configure the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUBBLE_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #with pull up no need for external resisitors


try:  
    while True:
         if ( GPIO.input(BUBBLE_SWITCH_PIN) == CLOSED_DOOR ):
              if (door_state == False or door_state == 'open'):
				  door_state = 'closed'
              if (old_door_state != door_state):
				print "door closed."
				old_door_state = door_state
				time.sleep(0.1) #need slight delay to avoid double readings
    
         elif ( GPIO.input(BUBBLE_SWITCH_PIN) == OPEN_DOOR ):
              if (door_state == False or door_state == 'closed'):
				  door_state = 'open'
              if (old_door_state != door_state):
				print "door open."
				old_door_state = door_state
				time.sleep(0.1) #need slight delay to avoid double readings
				
finally:
    print('Cleaning up GPIO')
    GPIO.cleanup()
