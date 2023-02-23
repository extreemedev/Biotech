# Multi-services docker Bioinformatics Pipeline for Assembly and Genomic Annotation

## Project `biopipeline-novnc` developed by [extreemedev][this-github-matt] & [adriIT][this-github-adri]

[Docker Hub][this-docker] - [Git Hub][this-github] - [Changelog][this-changelog] - [Wiki][this-wiki] - [Hierarchy][this-wiki-image-hierarchy]

***

**Attention!** The repository [accetto/xubuntu-vnc-novnc][this-github-novnc] is **retired** and **archived**. It will not be developed any further and the related images on Docker Hub will not be rebuilt any more. They will phase out and they will be deleted after becoming too old.


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

![image](https://drive.google.com/uc?export=view&id=1FbzpwJHxemwkqwWJSCFBQi9BnSDY1KgF)

This project's goal is to create a user friendly environment where anyone can easily use the pipeline. It consists of a Docker Compose file which manages every softwares and microservices. Periodically (every 5 seconds) the host-system will check if the working directory contains the needed file to begin the pipeline, then will proceed automatically to start it, using a Python script. In the working directory then, the main program will add some specific folders named after the softwares, that will contain the output files generated.    

***

## Dockerfile image `xubuntu-novnc-biotech:latest`

![image](https://drive.google.com/uc?export=view&id=1XoLgU-GS7JlHbnqV2O3f1va3YV1BvC5l)

Our Dockerfile image `monitor` is based on [accetto/xubuntu-vnc-novnc][this-github-novnc] published image. This new custom image includes a bunch of jre and python installations and moreover some custom enviroment settings, which may let the user be easy using this NoVNC system. It also includes a [FastQC][this-man-fastqc] interactive installation. Just for debug purpose, you can find these installations under the path: `/otp/bioprograms`, but it's highly recommended not to operate inside this directory.

***

## Docker compose structure

![image](https://drive.google.com/uc?export=view&id=1oNtKLn59Hs02c0ZFXlcRIXqALaV3huuS)

This project repository contains resources for building various Docker images based on [Ubuntu][docker-ubuntu] with [Xfce][xfce] desktop environment and [VNC][tigervnc]/[noVNC][novnc] servers for headless use.
The resources for the individual images and their variations are stored in the subfolders of the [Git Hub][this-github] repository and the image features are described in the individual README files. Additional descriptions can be found in the common project [Wiki][this-wiki].
All images are part of a growing [image hierarchy][this-wiki-image-hierarchy].

This `docker-compose.yml` file defines multiple services for different bioinformatics tools, each running on its own container. Some of these services have bind mounts, which allow them to access files and scripts on the host system. The containers are set to automatically restart and they are all part of the same network called bionet.
Every single container is bound to the same working directory, generally on `/scripts`, in order to generate the expected outputs for each process.
The main container, `monitor` service, runs a desktop environment and exposes ports 25901 and 26901 for remote access. It runs the previous built Dockerfile image `xubuntu-novnc-biotech:latest`, and it has a Graphic User Interface where the user can easily work into. Inside this last one, the user has root privileges to enable file actions.

***

## Docker containers and images

![image](https://drive.google.com/uc?export=view&id=16CMbOzqP0cU1Q03tMS0pyaulOHpAx7IE)

Here's a list of the container's names used in `docker-compose.yml`, associated to the docker images retrievable on https://hub.docker.com. This list is provided in alphabetical order except for monitor (main service):

- [monitor][this-docker-xubuntu-vnc-novnc]: This provides a fully functional Xubuntu desktop environment accessible through a web browser via the noVNC client. The container includes a web-based VNC viewer and a lightweight window manager, as well as various tools and applications commonly used in a Linux environment. The container is designed to be easily customizable and supports several configuration options, such as enabling clipboard sharing and mounting external volumes. By running the container, users can access a virtual Linux desktop environment from anywhere with a web browser, without the need for a local VNC client or additional software installations.

- [biopython][this-docker-biopython]: This container is used to run [fetchClusterSeqs.py][github-fetchcluster] which is a Python script that helps retrieve DNA sequences from a FASTA file based on a list of cluster IDs. The script takes as input a FASTA file and a text file containing the cluster IDs, and outputs a new FASTA file containing only the sequences with IDs that match the cluster IDs in the input file. The script also allows for filtering sequences based on their length and can output the sequences in reverse-complement form if desired. This service is provided by [Adam Taranto][github-adamtaranto]

- [busco][this-docker-busco]: BUSCO is a bioinformatics tool used to evaluate the completeness and quality of a gene assembly or genome sequence set. It compares genome sequences with a set of universal single-copy orthologs to identify missing or duplicated genes.

- [cdhit][this-docker-cdhit]: CD-HIT-est is a bioinformatics tool used for clustering and comparing protein or nucleotide sequences. It can be used to reduce the complexity of a large sequence dataset by clustering sequences that are highly similar, thereby speeding up subsequent analyses.

- [corset][this-docker-corset]: Corset is a bioinformatics tool used for clustering and annotating transcriptome assemblies from RNA-Seq data. It identifies clusters of transcripts that represent putative genes and can annotate these clusters with functional information.

- [fastqc][this-docker-fastqc]: FastQC is a bioinformatics tool used for quality control of high-throughput sequencing data. It provides a graphical interface for the visualization and assessment of sequence quality, adapter contamination, GC content, and other metrics.

- [hisat][this-docker-hisat2]: HISAT2 is an RNA-Seq sequence alignment software used to identify expressed transcripts in a specific experimental condition, quantify gene expression, and discover novel splicing variants. It can handle sequences with a high error rate and efficiently identify multiple alignments.

- [spades][this-docker-spades]: SPAdes is a genome assembly software designed specifically for RNA sequencing data. It can perform both de novo assembly of the transcriptome and genome-guided assembly using a reference genome. SPAdes can handle various types of RNA sequencing data, including stranded, non-stranded, paired-end, and single-end reads, and is capable of resolving complex transcript structures and alternative splicing events.

- [transdecoder][this-docker-transdecoder]: TransDecoder is a software package used for the identification of coding regions within de novo transcriptome assemblies, such as those generated from RNA-Seq data. It can predict the likely coding regions of the transcripts, including those for full-length proteins, as well as the locations of start and stop codons. TransDecoder can also identify potential coding regions from genomic sequences that lack annotation, using evidence from expressed sequences.

- [trimmomatic][this-docker-trimmomatic]: Trimmomatic is a software tool used for the quality control and preprocessing of high-throughput sequencing data, particularly for Illumina data. It can perform various trimming tasks, such as removing low quality bases, adapter sequences, and contaminant sequences, and can also trim reads based on length and quality. Trimmomatic can improve the accuracy of downstream analyses and reduce errors caused by sequencing artifacts and low-quality reads.

***

## Working Directory

These base images already include commonly used utilities **ping**, **wget**, **zip**, **unzip**, **sudo**, [curl][curl], [git][git] and also the current version of [jq][jq] JSON processor.
Additional components and applications can be easily added by the user because **sudo** is supported.


***

## Python Package Utils

### Can be found here: [/utils/][this-github-utils]
  
Contains utilities that make building the images more convenient and helps out the user get a full clean installation and uninstallation, plus various settings:

- `utils/pipeManager/`  

  Includes every file needed for the first installation and the initial setup. **It is severerly recommended to not touch or modify any of these files.**
  

- `utils/pipePackage/`  

  Includes every file or extension needed for the pipeline to work properly. **It is severerly recommended to not touch or modify any of these files.**
  

- `utils/util-hdx.sh`  

  Displays the file head and executes the chosen line, removing the first occurrence of '#' and trimming the line from left first. Providing the line number argument skips the interaction and executes the given line directly.The comment lines at the top of included Dockerfiles are intended for this utility.
  The utility displays the help if started with the `-h` or `--help` argument. It has been developed using my other utilities `utility-argbash-init.sh` and `utility-argbash.sh`, contained in the [accetto/argbash-docker][accetto-github-argbash-docker-utils] Git Hub repository, from which the [accetto/argbash-docker][accetto-docker-argbash-docker] Docker image is built.

- `utils/util-refresh-readme.sh`  

  This script can be used for updating the `version sticker` badges in README files. It is intended for local use before publishing the repository.
  The script does not include any help, because it takes only a single argument - the path where to start searching for files (default is `../docker`).

***

## Installation

**Attention!** To install this full pipeline service, you'll need to be **root** or a **sudoer user**.

Now, in order to install the entire service, move inside `/utils/pipeManager/` and run the python installing script, with the following command:
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

## noVNC Web Access
**Watch out!** In order to access this web page, you have to host the service, following the next step:

Please, move into this directory `/docker/xubuntu-novnc-biotech/` and run this command in the terminal:
```
docker compose up --build -d
```
or you can simply just do it, **(Only on VS Code)** by right-clicking on `docker-compose.yml` and then clicking `Compose Up` thanks to Visual Studio Code Docker Extension


After running `compose up` on the `docker-compose.yml` file, we are ready to access the web page linked [http://localhost:26901/vnc.html?password=headless][novnc-web] and connect remotely and locally to the service running on the host machine in question.

![](https://drive.google.com/uc?export=view&id=1LafYdoqD8g14eHKIaf9c599HwPmBvwtE)

**Remind**: once you execute this command, this docker-compose, will automatically restart every single container if some problems are experienced. Moreover this compose service will be running at every system boot/startup/restart. To avoid this you can simply run this command in the terminal:
```
docker compose down
```

***

## Running the service and Usage

**Watch out!** Before running and using the service you'll need to perform the previous step.



Now, you are ready to run the service and suddenly execute the pipeline. Everytime you will need to execute the pipeline, open the terminal and please type the following command:
```
sudo service pipeline start
```

***

## Uninstallation

**Attention!** To uninstall this full pipeline service, you'll need to be **root** or a **sudoer user**. Consider that, uninstalling this service, will also destroy your cloned repository.

If you have the need to remove this service, or you are having trouble with filesystem conflicts or anything else, please use our one-step uninstall script. Please move inside `/utils/pipeManager/` and use the following command:
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

- [X] Remove console print from pipeChooser.py

- [X] pipePackage: move all desired pipe extensions inside /opt/pipeline/lib

- [X] Dockerfile: move pipeScript in scripts into monitor /opt/

- [ ] Dockerfile: mettere gli eseguibili sul desktop di novnc. Basta caricare in hooks, i file .desktop, copiarli nel dockerfile e dare i permessi di esecuzione

- [ ] FetchCluster: move it inside Biopython (embedded)

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
[this-github]:https://github.com/extreemedev/Biotech
[this-github-matt]: https://github.com/extreemedev/
[this-github-adri]: https://github.com/adriIT/
[this-github-novnc]: https://github.com/accetto/xubuntu-vnc-novnc/
[this-changelog]: https://github.com/accetto/xubuntu-vnc-novnc/blob/master/CHANGELOG.md


[this-wiki]: https://github.com/accetto/xubuntu-vnc-novnc/wiki
[this-wiki-image-hierarchy]: https://github.com/accetto/xubuntu-vnc-novnc/wiki/Image-hierarchy
[this-issues]: https://github.com/accetto/xubuntu-vnc-novnc/issues
[this-github-utils]: https://github.com/extreemedev/Biotech/tree/master/utils
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


[this-docker-busco]: https://hub.docker.com/r/ezlabgva/busco
[this-docker-biopython]: https://hub.docker.com/r/biocontainers/biopython
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


[github-fetchcluster]: https://github.com/Adamtaranto/Corset-tools/blob/master/fetchClusterSeqs.py
[github-adamtaranto]: https://github.com/Adamtaranto
[novnc-web]: http://localhost:26901/vnc.html?password=headless