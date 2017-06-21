#!//bin/sh

############################################################
# on_reboot.sh shell script
# Stuart Simpson Jun 21/2017
# 
# Inital script setup instructions:
# 
# have to add line to /etc/rc.local
# sudo nano /etc/rc.local
# add this line before exit 0
# home/pi/garage-door-controller/on_reboot.sh &
#
# also chmod +x on_reboot.sh (and for the python programs.)
############################################################

# on_reboot.sh
# 
# Shell script to run the garage door controller website 
# and the tweety_pi_emailer.py program upon boot.
# now working.

#have to cd into the directories even though absolute path provided.  strange.

sleep 10

#start the tweety_pi_emailer program

cd /home/pi/garage-door-controller/tweety_pi_emailer/
sudo python /home/pi/garage-door-controller/tweety_pi_emailer/tweety_pi_emailer.py &

sleep 10 

#start the modified garage door controller program that puts the door status on a locally hosted webpage

cd /home/pi/garage-door-controller
sudo python /home/pi/garage-door-controller/controller.py &

