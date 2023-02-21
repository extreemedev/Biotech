# Multi-services docker Bioinformatics Pipeline for Assembly and Genomic Annotation

## Project `/biopipeline-novnc` developed by [extreemedev][this-github-matt] & [adriIT][this-github-adri]

[Docker Hub][this-docker] - [Git Hub][this-github] - [Changelog][this-changelog] - [Wiki][this-wiki] - [Hierarchy][this-wiki-image-hierarchy]

***

**Attention!** The repository [accetto/ubuntu-vnc-novnc][this-github-novnc] is **retired** and **archived**. It will not be developed any further and the related images on Docker Hub will not be rebuilt any more. They will phase out and they will be deleted after becoming too old.


![badge-github-release][badge-github-release]
![badge-github-release-date][badge-github-release-date]
![badge-github-stars][badge-github-stars]
![badge-github-forks][badge-github-forks]
![badge-github-open-issues][badge-github-open-issues]
![badge-github-closed-issues][badge-github-closed-issues]
![badge-github-releases][badge-github-releases]
![badge-github-commits][badge-github-commits]
![badge-github-last-commit][badge-github-last-commit]


***

## Overview

This project's goal is to create a user friendly environment where anyone can easily use the pipeline. It consists of a Docker Compose file which manages every softwares and microservices. Periodically (every 5 seconds) the host-system will check if the working directory contains the needed file to begin the pipeline, then will proceed automatically to start it, using a Python script. In the working directory then, the main program will add some specific folders named after the softwares, that will contain the output files generated.    

***

## Dockerfile image `xubuntu-novnc-biotech:latest`

Our Dockerfile image `monitor` is based on [accetto/ubuntu-vnc-novnc][this-github-novnc] published image. This new custom image includes a bunch of jre and python installations and moreover some custom enviroment settings, which may let the user be easy using this NoVNC system. It also includes a [FastQC][this-man-fastqc] interactive installation. Just for debug purpose, you can find these installation under the path: `/otp/bioprograms`, but it's highly recommended not to operate inside this directory.

***

## Docker compose structure

![image](https://drive.google.com/uc?export=view&id=1oNtKLn59Hs02c0ZFXlcRIXqALaV3huuS)

This project repository contains resources for building various Docker images based on [Ubuntu][docker-ubuntu] with [Xfce][xfce] desktop environment and [VNC][tigervnc]/[noVNC][novnc] servers for headless use.

The resources for the individual images and their variations are stored in the subfolders of the [Git Hub][this-github] repository and the image features are described in the individual README files. Additional descriptions can be found in the common project [Wiki][this-wiki].

All images are part of a growing [image hierarchy][this-wiki-image-hierarchy].

In the `docker-compose.yml` file containers speak onto a bridge network, and each of them has its unique purpose, with its unique image installed, as specified on the pipeline workflow. Every single container is bound to the same working directory, generally on `/scripts`, in order to generate the expected outputs for each process.
The main container, named `monitor`, that runs the previous built Dockerfile image `xubuntu-novnc-biotech:latest`, has the GUI where the user can easily work into. Inside this last one, the user has root privileges to enable file actions. Moreover `monitor` is the only one which has access to localhost on port 26901, due to the bind with the internal container port 6901, that enables noVNC display on browser.

***

## Docker containers and images 

Here's a list of the containers name we used associated to the docker images retrievable on https://hub.docker.com:

-[monitor][this-docker-xubuntu-vnc-novnc]

-[busco][this-docker-busco]

-[cdhit][this-docker-cdhit]

-[corset][this-docker-corset]

-[fastqc][this-docker-fastqc]

-[hisat][this-docker-hisat2]

-[spades][this-docker-spades]

-[transdecoder][this-docker-transdecoder]

-[trimmomatic][this-docker-trimmomatic]

***

## Working Directory

***

#### [xubuntu-vnc-novnc][this-github-xubuntu-vnc-novnc]

Contains resources for building [accetto/xubuntu-vnc-novnc][this-docker-xubuntu-vnc-novnc] base images.

The images are streamlined and simplified versions of my other images [accetto/ubuntu-vnc-xfce][accetto-docker-ubuntu-vnc-xfce].

Several variations are available, including the one supporting overriding both the container user and the user group.

These base images already include commonly used utilities **ping**, **wget**, **zip**, **unzip**, **sudo**, [curl][curl], [git][git] and also the current version of [jq][jq] JSON processor.

Additional components and applications can be easily added by the user because **sudo** is supported.



#### [xubuntu-vnc-novnc-chromium][this-github-xubuntu-vnc-novnc-chromium]
  
Contains resources for building [accetto/xubuntu-vnc-novnc-chromium][this-docker-xubuntu-vnc-novnc-chromium] images with the open-source [Chromium][chromium] web browser.

#### [xubuntu-vnc-novnc-firefox][this-github-xubuntu-vnc-novnc-firefox]
  
Contains resources for building [accetto/xubuntu-vnc-novnc-firefox][this-docker-xubuntu-vnc-novnc-firefox] images with the current [Firefox Quantum][firefox] web browser.

Several variations are available, including the one supporting easy pre-configuration and copying of personal Firefox user preferences.

The images are streamlined and simplified versions of my other images [accetto/ubuntu-vnc-xfce-firefox-plus][accetto-docker-ubuntu-vnc-xfce-firefox-plus] and [accetto/ubuntu-vnc-xfce-firefox-default][accetto-docker-ubuntu-vnc-xfce-firefox-default].

***

## Python Package Utils

### Can be found here: [/utils/][this-github-utils]
  
Contains utilities that make building the images more convenient and helps out the user get a full clean installation and uninstallation, plus various settings:

- `utils/pipeInstall/`  

  Displays the file head and executes the chosen line, removing the first occurrence of '#' and trimming the line from left first. Providing the line number argument skips the interaction and executes the given line directly.
  

- `utils/pipePackage/`  

  Displays the file head and executes the chosen line, removing the first occurrence of '#' and trimming the line from left first. Providing the line number argument skips the interaction and executes the given line directly.
  

- `utils/util-hdx.sh`  

  Displays the file head and executes the chosen line, removing the first occurrence of '#' and trimming the line from left first. Providing the line number argument skips the interaction and executes the given line directly.
  
  The comment lines at the top of included Dockerfiles are intended for this utility.

  The utility displays the help if started with the `-h` or `--help` argument. It has been developed using my other utilities `utility-argbash-init.sh` and `utility-argbash.sh`, contained in the [accetto/argbash-docker][accetto-github-argbash-docker-utils] Git Hub repository, from which the [accetto/argbash-docker][accetto-docker-argbash-docker] Docker image is built.

- `utils/util-refresh-readme.sh`  
  
  This script can be used for updating the `version sticker` badges in README files. It is intended for local use before publishing the repository.

  The script does not include any help, because it takes only a single argument - the path where to start searching for files (default is `../docker`).

***

## Installation

**Attention!** To install this full pipeline service, you'll need to be **root** or a **sudoer user**.

Now, in order to install the entire service, move inside `/utils/pipeInstall/` and run the python installing script, with the following command:
```
python3 pipeInstall.py
```
All needed dependancies will be installed and this tree directory structure will be created on your operative system (starting from the root):
```
/opt/
  |
  ├─ pipeline/
        |
        ├─ bin/
        |
        ├─ etc/
        |
        ├─ lib/
        |
        ├─ log/
        |
        ├─ opt/
        |
        ├─ var/
```

## Issues

If you have found a problem or you just have a question, please check the [Issues][this-issues] and the [Wiki][this-wiki] first. Please do not overlook the closed issues.

If you do not find a solution, you can file a new issue. The better you describe the problem, the bigger the chance it'll be solved soon.

***

## Running the service and Usage
**Watch out!** Before running and using the service you'll need to perform the previous step.

Now, you are ready to run the service and suddenly execute the pipeline. Everytime you will need to execute the pipeline, please type the following command:
```
sudo service pipeline start
```

***

## Uninstallation

**Attention!** To uninstall this full pipeline service, you'll need to be **root** or a **sudoer user**. Consider that, uninstalling this service, will also destroy your cloned repository.

If you have the need to remove this service, or you are having trouble with filesystem conflicts or anything else, please use our one-step uninstall script. Please move inside `/utils/pipeInstall/` and use the following command:
```
python3 pipeUninstall.py
```
The service will be removed from `/etc/init.d`, all files will be deleted and the tree directory structure will be purged. If you would like to reinstall it, you'll have to clone this repository again and repeat the process of installation.
***

## Credits

Credit goes to all the people, who contribute and provided this big cluster of docker image and resources:

***

## To-Do-List

- [X] Administrate Monitor/FastQC

- [X] Create logger/log files

- [X] Check the service status (def .py) within n-start of pipeline.service

- [X] Resolve def readWorkdir()

- [ ] pipePackage: move all desired pipe extensions inside /opt/pipeline/lib

- [ ] FetchCluster: move it inside Biopython (embedded)

- [ ] Dockerfile: move pipeScript in scripts into monitor /opt/

- [ ] Line 30 pipeFull.py

- [ ] Optimize logger stout lines

- [ ] Give back to user command prompt

- [ ] Automated start and restart of Compose Service

- [ ] Pipeline loading script

- [ ] Echo in pipeline.sh ("\n")

- [ ] Line 11 in pipeline.sh

- [ ] Installation directory Dockerfile programs and sources

- [ ] Resolve Busco problem

- [ ] Check pull & installation (before the exam)



[this-docker]: https://hub.docker.com/u/mattallev

[this-github-matt]: https://github.com/extreemedev/
[this-github-adri]: https://github.com/adriIT/
[this-github-novnc]: https://github.com/accetto/xubuntu-vnc-novnc/
[this-changelog]: https://github.com/accetto/xubuntu-vnc-novnc/blob/master/CHANGELOG.md

[this-wiki]: https://github.com/accetto/xubuntu-vnc-novnc/wiki
[this-wiki-image-hierarchy]: https://github.com/accetto/xubuntu-vnc-novnc/wiki/Image-hierarchy

[this-issues]: https://github.com/accetto/xubuntu-vnc-novnc/issues

[this-github-utils]: https://github.com/accetto/xubuntu-vnc-novnc/tree/master/utils/

[this-github-xubuntu-vnc-novnc]: https://github.com/accetto/xubuntu-vnc-novnc/tree/master/docker/xubuntu-vnc-novnc/
[this-docker-xubuntu-vnc-novnc]: https://hub.docker.com/r/accetto/xubuntu-vnc-novnc/

[this-github-xubuntu-vnc-novnc-chromium]: https://github.com/accetto/xubuntu-vnc-novnc/tree/master/docker/xubuntu-vnc-novnc-chromium/
[this-docker-xubuntu-vnc-novnc-chromium]: https://hub.docker.com/r/accetto/xubuntu-vnc-novnc-chromium/

[this-github-xubuntu-vnc-novnc-firefox]: https://github.com/accetto/xubuntu-vnc-novnc/tree/master/docker/xubuntu-vnc-novnc-firefox/
[this-docker-xubuntu-vnc-novnc-firefox]: https://hub.docker.com/r/accetto/xubuntu-vnc-novnc-firefox/

[accetto-docker-ubuntu-vnc-xfce]: https://hub.docker.com/r/accetto/ubuntu-vnc-xfce
[accetto-docker-ubuntu-vnc-xfce-firefox-default]: https://hub.docker.com/r/accetto/ubuntu-vnc-xfce-firefox-default
[accetto-docker-ubuntu-vnc-xfce-firefox-plus]: https://hub.docker.com/r/accetto/ubuntu-vnc-xfce-firefox-plus

[accetto-github-xubuntu-vnc]: https://github.com/accetto/xubuntu-vnc/
[accetto-xubuntu-vnc-wiki-image-hierarchy]: https://github.com/accetto/xubuntu-vnc/wiki/Image-hierarchy

[accetto-ubuntu-vnc-xfce-g3]: https://github.com/accetto/ubuntu-vnc-xfce-g3

[accetto-docker-ubuntu-vnc-xfce-g3]: https://hub.docker.com/r/accetto/ubuntu-vnc-xfce-g3
[accetto-docker-ubuntu-vnc-xfce-chromium-g3]: https://hub.docker.com/r/accetto/ubuntu-vnc-xfce-chromium-g3
[accetto-docker-ubuntu-vnc-xfce-firefox-g3]: https://hub.docker.com/r/accetto/ubuntu-vnc-xfce-firefox-g3

[accetto-docker-argbash-docker]: https://hub.docker.com/r/accetto/argbash-docker
[accetto-github-argbash-docker-utils]: https://github.com/accetto/argbash-docker/tree/master/utils

[docker-ubuntu]: https://hub.docker.com/_/ubuntu/

[curl]: http://manpages.ubuntu.com/manpages/bionic/man1/curl.1.html
[git]: https://git-scm.com/
[inkscape]: https://inkscape.org/
[jq]: https://stedolan.github.io/jq/
[firefox]: https://www.mozilla.org
[git]: https://git-scm.com/
[novnc]: https://github.com/kanaka/noVNC
[novnc-releases]: https://github.com/novnc/noVNC/releases
[tigervnc]: http://tigervnc.org
[tigervnc-releases]: https://github.com/TigerVNC/tigervnc/releases
[xfce]: http://www.xfce.org


[this-docker-xubuntu-vnc-novnc]: https://hub.docker.com/r/accetto/xubuntu-vnc-novnc/
[this-docker-busco]: https://hub.docker.com/r/ezlabgva/busco
[this-docker-cdhit]: https://hub.docker.com/r/chrishah/cdhit
[this-docker-corset]: https://hub.docker.com/r/mdiblbiocore/corset
[this-docker-fastqc]: https://hub.docker.com/r/staphb/fastqc
[this-docker-hisat2]: https://hub.docker.com/r/nanozoo/hisat2
[this-docker-spades]: https://hub.docker.com/r/staphb/spades
[this-docker-transdecoder]: https://hub.docker.com/r/biocrusoe/transdecoder
[this-docker-trimmomatic]: https://hub.docker.com/r/staphb/trimmomatic

[this-github-corset]: https://github.com/Oshlack/Corsethttps://code.google.com/archive/p/corset-project/
[this-github-transdecoder]: https://github.com/TransDecoder/TransDecoder/wiki
[this-github-trimmomatic]: https://github.com/usadellab/Trimmomatic
[this-github-xubuntu-vnc-novnc]: https://github.com/accetto/xubuntu-vnc-novnc/tree/master/docker/xubuntu-vnc-novnc/

[this-man-busco]: https://busco.ezlab.org/busco_userguide.html
[this-man-cdhit]: https://www.bioinformatics.org/cd-hit/
[this-man-fastqc]: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
[this-man-hisat2]: http://daehwankimlab.github.io/hisat2/
[this-man-spades]: https://cab.spbu.ru/files/release3.14.1/manual.html


<!-- github badges -->

[badge-github-release]: https://badgen.net/github/release/extreemedev/Biotech?icon=github&label=release

[badge-github-release-date]: https://img.shields.io/github/release-date/extreemedev/Biotech?logo=github

[badge-github-stars]: https://badgen.net/github/stars/extreemedev/Biotech?icon=github&label=stars

[badge-github-forks]: https://badgen.net/github/forks/extreemedev/Biotech?icon=github&label=forks

[badge-github-releases]: https://badgen.net/github/releases/extreemedev/Biotech?icon=github&label=releases

[badge-github-commits]: https://badgen.net/github/commits/extreemedev/Biotech?icon=github&label=commits

[badge-github-last-commit]: https://badgen.net/github/last-commit/extreemedev/Biotech?icon=github&label=last%20commit

[badge-github-closed-issues]: https://badgen.net/github/closed-issues/extreemedev/Biotech?icon=github&label=closed%20issues

[badge-github-open-issues]: https://badgen.net/github/open-issues/extreemedev/Biotech?icon=github&label=open%20issues


