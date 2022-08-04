#!/bin/bash

mkdir /var/run/sshd

#
# if there is a self.pem certificate file on /configs/certs, let's use it
# instead of the cert compiled into the docker container
#
cp /configs/certs/self.pem /noVNC/
chmod 600 /noVNC/self.pem

#
# settings files for X and application(s)
#
mkdir -p /home/ubuntu/Desktop
cp -r /configs/desktop-items/* /home/ubuntu/Desktop/
mkdir -p /home/ubuntu/.local/share/applications/
cp -r /configs/desktop-items/* /home/ubuntu/.local/share/applications/
mkdir -p /home/ubuntu/.config
cp -r /configs/openbox/* /home/ubuntu/.config/

# make sure they own their home directory
chown -R ubuntu ~ubuntu ; chgrp -R users ~ubuntu

# set the passwords for the user and the x11vnc session
# based on environment variables (if present), otherwise roll with
# the defaults from the Dockerfile build. 
#
if [ ! -z $UBUNTUPASS] 
then
  /bin/echo "ubuntu:$UBUNTUPASS" | /usr/sbin/chpasswd
  UBUNTUPASS=''
fi

if [ ! -z $VNCPASS ] 
then
  /usr/bin/x11vnc -storepasswd $VNCPASS  /home/root/.vnc/passwd
  VNCPASS=''
fi

exit 0
