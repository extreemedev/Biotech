FROM accetto/xubuntu-vnc-novnc

USER root
#RUN apt-get update && apt-get install -y sudo lsb-core && rm -rf /var/lib/apt/lists/*

RUN wget http://cab.spbu.ru/files/release3.14.1/SPAdes-3.14.1-Linux.tar.gz
RUN tar -xzf SPAdes-3.14.1-Linux.tar.gz
RUN cd SPAdes-3.14.1-Linux/bin/


# Update index (again) and install OpenModelica 
RUN apt-get update && rm -rf /var/lib/apt/lists/* && apt-get clean 

#RUN apt install omlib-.* # Installs optional Modelica libraries (most have not been tested with OpenModelica)

USER 1000