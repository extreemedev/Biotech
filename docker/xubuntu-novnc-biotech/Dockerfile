FROM accetto/xubuntu-vnc-novnc:latest

USER root

COPY ./src/xfce-teal.jpg /usr/share/backgrounds/xfce/

COPY ./hooks/fastQC.sh /home/headless/BioPrograms/

#RUN /home/headless/BioPrograms/fastQC.sh

#Various sets
RUN sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1 \
    && sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 2

#Various install
RUN sudo apt-get update && sudo apt-get install -y \
    default-jre \
    python3-pip \
    python3-tk

RUN pip3 install easygui


##FastQC
RUN wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip \
    && unzip fastqc_v0.11.9.zip -d /home/headless/BioPrograms \
    && rm -r fastqc_v0.11.9.zip \
    && chmod 755 /home/headless/BioPrograms/FastQC/fastqc \
    && sudo ln -s /home/headless/BioPrograms/FastQC/fastqc /usr/local/bin/fastqc \
    && sudo ln -s /home/headless/Desktop/fastqc.desktop /usr/share/applications/fastqc.desktop
    #importante questo sopra, serve a collegare nella page delle applicazioni, ed ha anche il potere di lanciare
#
#
#
##SPAdes-3.14.1
#RUN wget http://cab.spbu.ru/files/release3.14.1/SPAdes-3.14.1-Linux.tar.gz \
#    && tar -xzf SPAdes-3.14.1-Linux.tar.gz --directory ~/BioPrograms --transform 's!^[^/]\+\($\|/\)!SPAdes-3.14.1\1!' \
#    #&& ln -s ~/BioPrograms/SPAdes-3.14.1/bin/ ~/BioPrograms/SPAdes-3.14.1/share/ /usr \
#    && rm -r SPAdes-3.14.1-Linux.tar.gz
#
#
##Busco
#RUN git clone https://gitlab.com/ezlab/busco.git ~/BioPrograms/busco \
#    && cd ~/BioPrograms/busco && python3 setup.py install --user \
#    && cd
#
#
##Corset
#RUN wget https://github.com/Oshlack/Corset/releases/download/version-1.09/corset-1.09-linux64.tar.gz \
#    && tar -xzf corset-1.09-linux64.tar.gz --directory ~/BioPrograms --transform 's!^[^/]\+\($\|/\)!corset-1.09\1!' \
#    && rm -r corset-1.09-linux64.tar.gz
#

#Clean
RUN apt-get update && rm -rf /var/lib/apt/lists/* && apt autoremove && apt-get clean 


USER 1001