FROM accetto/xubuntu-vnc-novnc:latest

USER root

COPY ./xfce-teal.jpg /usr/share/backgrounds/xfce/


#       ░██████╗░█████╗░███████╗████████╗░██╗░░░░░░░██╗░█████╗░██████╗░███████╗
#       ██╔════╝██╔══██╗██╔════╝╚══██╔══╝░██║░░██╗░░██║██╔══██╗██╔══██╗██╔════╝
#       ╚█████╗░██║░░██║█████╗░░░░░██║░░░░╚██╗████╗██╔╝███████║██████╔╝█████╗░░
#       ░╚═══██╗██║░░██║██╔══╝░░░░░██║░░░░░████╔═████║░██╔══██║██╔══██╗██╔══╝░░
#       ██████╔╝╚█████╔╝██║░░░░░░░░██║░░░░░╚██╔╝░╚██╔╝░██║░░██║██║░░██║███████╗
#       ╚═════╝░░╚════╝░╚═╝░░░░░░░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝



#Various install
RUN sudo apt install \
    default-jre



#Fastqc
RUN wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip \
    && unzip fastqc_v0.11.9.zip -d ~/BioPrograms\
    && rm -r fastqc_v0.11.9.zip \
    && chmod 755 ~/BioPrograms/FastQC/fastqc \
    && sudo ln -s ~/BioPrograms/FastQC/fastqc /usr/local/bin/fastqc \
    && sudo ln -s ~/Desktop/fastqc.desktop /usr/share/applications/fastqc.desktop
    #importante questo sopra, serve a collegare nella page delle applicazioni, ed ha anche il potere di lanciare TOP



#SPAdes-3.14.1
RUN wget http://cab.spbu.ru/files/release3.14.1/SPAdes-3.14.1-Linux.tar.gz \
    && tar -xzf SPAdes-3.14.1-Linux.tar.gz \
    && cp -r SPAdes-3.14.1-Linux/bin/ SPAdes-3.14.1-Linux/share/ /usr \
    && rm -r SPAdes-3.14.1-Linux*


#Trimmomatic






#       ░█████╗░██╗░░░░░███████╗░█████╗░███╗░░██╗
#       ██╔══██╗██║░░░░░██╔════╝██╔══██╗████╗░██║
#       ██║░░╚═╝██║░░░░░█████╗░░███████║██╔██╗██║
#       ██║░░██╗██║░░░░░██╔══╝░░██╔══██║██║╚████║
#       ╚█████╔╝███████╗███████╗██║░░██║██║░╚███║
#       ░╚════╝░╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝

RUN apt-get update && rm -rf /var/lib/apt/lists/* && apt autoremove && apt-get clean 


USER 1001