#!/bin/bash
echo "#!/usr/bin/env xdg-open \

[Desktop Entry] \

Version=1.0 \

Type=Application \

Name=FastQC \

Comment= \

Exec=/home/headless/BioPrograms/FastQC/fastqc \

Icon= \

Path= \

Terminal=false \

StartupNotify=false" > /home/headless/Desktop/fastqc.desktop \
&& chmod +x /home/headless/Desktop/fastqc.desktop \
&& sudo ln -s /home/headless/BioPrograms/FastQC/fastqc /usr/local/bin/fastqc \
&& sudo ln -s /home/headless/Desktop/fastqc.desktop /usr/share/applications/fastqc.desktop \
&& cat /home/headless/Desktop/fastqc.desktop \