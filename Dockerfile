FROM ubuntu:14.04
LABEL Matteo Alleva & Adriano Giuliani <alleva.1889197@studenti.uniroma1.it>

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root

# setup our Ubuntu sources (ADD breaks caching)
RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main restricted universe multiverse\n\
deb http://archive.ubuntu.com/ubuntu trusty-updates main restricted universe multiverse\n\
deb http://archive.ubuntu.com/ubuntu trusty-backports main restricted universe multiverse\n\ 
deb http://security.ubuntu.com/ubuntu trusty-security main restricted universe multiverse \n\
"> /etc/apt/sources.list

# no Upstart or DBus
# https://github.com/dotcloud/docker/issues/1724#issuecomment-26294856
RUN apt-mark hold initscripts udev plymouth mountall
RUN dpkg-divert --local --rename --add /sbin/initctl && ln -sf /bin/true /sbin/initctl
RUN apt-get update \
    && apt-get upgrade -y

RUN apt-get install -y --force-yes --no-install-recommends \
        python-numpy \ 
        software-properties-common \
        wget \
        supervisor \
        openssh-server \
        pwgen \
        sudo \
        vim-tiny \
        net-tools \
        lxde \
        x11vnc \
        xvfb \
        gtk2-engines-murrine \
        ttf-ubuntu-font-family \
        firefox \
        xserver-xorg-video-dummy \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/supervisor/conf.d
RUN rm /etc/supervisor/supervisord.conf

#
# create a ubuntu user in the "ubuntu" group with sudo privs:
# RUN useradd --create-home --shell /bin/bash --user-group --groups adm,sudo ubuntu
#
# create a ubuntu user in the "users" group without sudo privs for the sake of some security
#
RUN useradd --create-home --shell /bin/bash --no-user-group --groups users ubuntu
RUN echo "ubuntu:badpassword" | chpasswd

ADD initialize.sh /
ADD supervisord.conf.xorg /etc/supervisor/supervisord.conf
EXPOSE 6080
EXPOSE 5900

#
# copy some default X configs into the user account
# note that if you mount an external volume to persist user accounts, 
# you will probably need to do this in an init script too because
# the external volume will mask whatever was done to the user directory
# when the container was built
#
ADD configs /configs
RUN cp -r /configs/desktop-items/* /usr/share/applications/ ; \
    mkdir -p ~ubuntu/.config ; \
    cp -r /configs/openbox/* ~ubuntu/.config/ ; \
    chown -R ubuntu ~ubuntu/.config ; \
    chgrp -R users ~ubuntu/.config 

# noVNC
ADD noVNC /noVNC/
# store a password for the VNC service
RUN mkdir /home/root
RUN mkdir /home/root/.vnc
RUN x11vnc -storepasswd foobar /home/root/.vnc/passwd
ADD xorg.conf /etc/X11/xorg.conf

#ENTRYPOINT ["/usr/bin/supervisord", "--nodaemon", "-c", "/etc/supervisor/supervisord.conf"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

