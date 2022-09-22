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

StartupNotify=false" > ~/Desktop/fastqc.desktop \
&& chmod +x ~/Desktop/fastqc.desktop \
&& printf "\nFile creato correttamente\n\n" \
&& sudo ln -s ~/Desktop/fastqc.desktop /usr/share/applications/fastqc.desktop \
&& cat ~/Desktop/fastqc.desktop \
&& printf "\n"