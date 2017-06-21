#software from:  https://github.com/andrewshilliday/garage-door-controller/

#installation instructions on there.

# http://192.168.0.18:8081/  shows webpage (need to change ip address depending upon the network, or use a name if registered the ip address. )
# http://127.0.0.1:8081/     shows webpage from localhost if we check on this machine.

# ifconfig to see ip address from terminal


# wifi configuration on top right corner of the screen.
# program autoboots from change to /etc/rc.local.  (sudo nano /etc/rc.local)
# add (cd ~pi/garage-door-controller; python controller.py) &
# before the end for rc.local


# see settings in config.json


