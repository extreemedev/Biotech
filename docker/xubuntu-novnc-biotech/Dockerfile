FROM accetto/xubuntu-vnc-novnc:latest

USER root

COPY ./src/xfce-teal.jpg /usr/share/backgrounds/xfce/

COPY ./src/pipe-workflow.png /opt/bioprograms/src/

# ---------------------------- BIOPIPELINE DESKTOP --------------------------- #

COPY ./hooks/pipeChooser.py /opt/bioprograms/

COPY ./hooks/BioPipeline.desktop /opt/bioprograms/

RUN chmod +x /opt/bioprograms/BioPipeline.desktop \
    && sudo ln -s /opt/bioprograms/BioPipeline.desktop /usr/share/applications/BioPipeline.desktop \
    && sudo ln -s /opt/bioprograms/BioPipeline.desktop /home/headless/Desktop/BioPipeline.desktop

# ------------------------------ FASTQC DESKTOP ------------------------------ #

COPY ./hooks/FastQC.desktop /opt/bioprograms/

RUN chmod +x /opt/bioprograms/FastQC.desktop \
    && sudo ln -s /opt/bioprograms/FastQC.desktop /usr/share/applications/FastQC.desktop \
    && sudo ln -s /opt/bioprograms/FastQC.desktop /home/headless/Desktop/FastQC.desktop

# -------------------------------- VARIOUS SET ------------------------------- #

RUN sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1 \
    && sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 2

# ------------------------------ VARIOUS INSTALL ----------------------------- #

RUN sudo apt-get update && sudo apt-get install -y \
    default-jre \
    python3-pip \
    python3-tk

RUN pip3 install easygui


# ---------------------------------- FASTQC ---------------------------------- #

RUN wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip \
    && unzip fastqc_v0.11.9.zip -d /opt/bioprograms/ \
    && rm -r fastqc_v0.11.9.zip \
    && chmod 755 /opt/bioprograms/FastQC/fastqc \
    && sudo ln -s /opt/bioprograms/FastQC/fastqc /usr/local/bin/fastqc \
    && sudo ln -s /home/headless/Desktop/fastqc.desktop /usr/share/applications/fastqc.desktop
    #importante questo sopra, serve a collegare nella page delle applicazioni, ed ha anche il potere di lanciare

# ----------------------------------- CLEAN ---------------------------------- #

RUN apt-get update && rm -rf /var/lib/apt/lists/* && apt autoremove && apt-get clean 


USER 1001