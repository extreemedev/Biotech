docker-novnc-template
=========================

This is a minimal image which will help you run X server with Openbox 
on the docker container and access it from ANY recent browser without 
requiring you to do any configuration on the client side.


## Why?

Provide system application accessible over the web without requiring 
the clients to install any  VNC client software, perhaps to provide 
remote access to applications running in docker containers for students 
doing coursework or researcher access to remote VMs/containers.


This container is a generic Ubuntu Linux with X, OpenBox, and NoVNC 
installed so that you can access the container via a GUI from your 
HTML5 web browser. 

It is very likely that you will want to augment this container with some 
additional applications. One way to do this is to map a directory 
containing the app into the container (read-only) and include some 
settings files so the app appears in the OpenBox GUI.

For example, suppose 
 - a matlab binary is located here:
```
      /srv/matlabR2014a
```
 - a desktop file (matlab.desktop) to define the matlab menu entry and desktop icon (and potentially other additions) are in the directory: 
```
      /srv/applications-desktop/
```
 - the user's persistent home directory is mounted as a volume from:
```
      /srv/homedirs/user1
```
 - a site certificate to allow encrypted connections is at:
```
      /srv/self.pem-myhost
```
 - you want to have users connect at port 6081
 - your server is named your.hostname.here
 - you want to set the password for login to the VNC session to somefunkypassword


You can run a container to do this by issuing the command:
```
docker run -d -t -p 6081:6080 \
   -e VNCPASS=somefunkypassword -v /srv/matlabR2014a:/matlabR2014a:ro \
   -v /srv/self.pem-myhost:/noVNC/self.pem \
   -v /srv/configs:/configs:ro  \
   -v /srv/homedirs/user1:/home/ubuntu -h your.hostname.here docker-novnc-template

```

## Building the container

First cd to the noVNC directory and create a self.pem certificate 
for noVNC because we want to force secure connections (via https and wss) 
between the user's web browser and the container. 

See the "Encrypted noVNC Sessions" section below for details on how to
set up the site certificate.

After you have a cert in self.pem, build the container with the command
```
sudo docker build -t docker-novnc-template .
```

Run using the default password from the Dockerfile build script:
```
sudo docker run -i -t -p 6081:6080 -h your.hostname.here docker-novnc-template
```

Better yet, run and set the passwords for VNC and user via environment variables:

```
sudo docker run -i -t -p 6081:6080 -e UBUNTUPASS=supersecret -e VNCPASS=secret \
   -h your.hostname.here docker-novnc-template
```
You need to specify the hostname to the container so that it matches the
site certificate that you configured noVNC with, or pedantic web browsers will
frighten users with scary warnings. 

Browse to
    https://your.hostname.here:6081/vnc.html
or
    https://your.hostname.here:6081/vnc_auto.html

You will be prompted for the vnc password which was set to 'foobar' in the
Dockerfile build. You'll probably want to change that and also change the 
hardcoded password ('badpassword') for the ubuntu account created 
in the build process by specifying passwords when you run the container.

Note that the user can skip the VNC password prompt if you redirect them to 

 https://your.host.here:6081/vnc.html?&encrypt=1&autoconnect=1&password=foobar


## Encrypted noVNC Sessions

To enable encrypted connections, you need to (at a minimum) create a 
noVNC self.pem certificate file as describe here: 
   https://github.com/kanaka/websockify/wiki/Encrypted-Connections

In other words do something like this

```
     openssl req -x509 -days 365 -nodes -newkey rsa:2048 -out self.pem -keyout self.pem 
```

Even better, get your private key signed by a known certificate authority,
so that users are not confronted with frightening warnings about untrusted sites. 


PROTIP: make sure that the read permissions are set to only allow root to read the
self.pem file, since you probably don't want users to get access to the private key.

## Xvfb vs XDummy/Xorg

There are two approaches that can be taken to set up a virtual framebuffer for the VNC
server. The Dockerfile.xvfb build will create a container that uses the ancient and venerable
Xvfb approach, while the Dockerfile.xorg creates a container the sets up an Xdummy framebuffer
in Xorg. For the Xorg approach, we also need to set up the xorg.conf config file so you might 
want take a look at the settings there. I'm keeping the Xvfb in this source for sentimental 
reasons. You probably want to run the xorg flavor since that is what I actually test.

The reason for considering the Xorg approach over Xvfb is Xorg+Xdummy support the randr 
dynamic screen resizing functions so there are fewer warnings thrown by apps like firefox,
and someday we might get clever about resizing on the fly, or take advantage of GLX extnesions.
See https://www.xpra.org/trac/wiki/Xdummy for details.

You'll need to copy Dockerfile.xvfb or Dockerfile.xorg to Dockerfile to build the appropriate
version for your situation.

## Misc Notes

The contents of /configs/openbox are copied to the user's ~/.config directory to put some 
reasonable default settings in place for the X environment when run inside a web browser. 
Reasonable means things like placing the dock at the top of the page so users don't have to 
scroll their web page to find it.

You can construct a URL that will automagically connect the user over an encrypted session
by passing appropriate parameters like this:

```
https://YOUR-HOST-HERE:6080/vnc.html?host=YOUR-HOST-HERE&port=6080&encrypt=1&autoconnect=1&password=XXXXX
```

To launch NoVNC with a password, put a password on the server with this:

```
    x11vnc -storepasswd badpassword /root/.vnc/passwd 
```

then use this startup.sh:

```
export DISPLAY=:1
Xvfb :1 -screen 0 1280x1024x16 &
openbox-session &
x11vnc -display :1 -bg -listen localhost -xkb -ncache 10 -ncache_cr  -passwd XXXXX
cd /root/noVNC && ./utils/launch.sh --vnc localhost:5900
```


## Extending

To add scripts to run at startup, modify the initialize.sh script we use to set up
user directories and launch services. The initialize.sh script is called by 
supervisord at container startup time. 

To add supervisord configs, add them to this folder:

```
/etc/supervisor/conf.d/
```

## Credits

Paim Pozhil's initial work on a NoVNC Docker container -- https://github.com/paimpozhil/docker-novnc

NoVNC -- http://kanaka.github.io/noVNC/

