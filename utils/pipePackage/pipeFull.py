import os
import sys
import multiprocessing

import docker

sys.path.insert(0, "/opt/pipeline/lib/")

import logging
import time

from alive_progress import alive_bar
from pipeExtensions import *
from pipeStatus import *


def Pipeline(pipename,file1,file2,threads=str(multiprocessing.cpu_count())):

    logger = logging.getLogger(__name__)  
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='/opt/pipeline/log/'+pipename+'.log', mode='w+')
    formatter = logging.Formatter('%(asctime)s : %(name)s  : %(funcName)s : %(levelname)s : %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
              "#                                Pipeline Started                              #\n"+ \
              "# ---------------------------------------------------------------------------- #\n")

    dir_scripts = readWorkdir()+"scripts/"      # CAMBIARE IN FAVORE DI OPT PIPELINE
    dir_pipe = pipename+"/"
    dir_fastqc = "FastQC"
    dir_trimmomatic = "Trimmomatic"
    dir_trimmomatic_trim = "Trimmomatic/trimmed_fastq"
    dir_trimmomatic_unpaired = "Trimmomatic/untrimmed_fastq"
    dir_spades = "Spades"
    dir_cdhit = "Cdhitest"
    dir_busco = "Busco"
    dir_hisat = "Hisat"
    dir_corset = "Corset"
    dir_transdecoder = "TransDecoder"
    createDir(dir_scripts+dir_pipe)
    createDir(dir_scripts+dir_pipe+dir_fastqc)
    createDirs((dir_scripts+dir_pipe+dir_trimmomatic, dir_scripts+dir_pipe+dir_trimmomatic_trim, dir_scripts+dir_pipe+dir_trimmomatic_unpaired))
    createDir(dir_scripts+dir_pipe+dir_cdhit)
    createDir(dir_scripts+dir_pipe+dir_busco)
    createDir(dir_scripts+dir_pipe+dir_hisat)
    createDir(dir_scripts+dir_pipe+dir_corset)
    os.system("sudo chmod -R 777 "+dir_scripts+dir_pipe)


    client = docker.from_env()


    print("init: Monitor")
    monitor = client.containers.get("monitor")
    monitor_msg = monitor.exec_run("echo Hello World!", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
    if int(monitor_msg.exit_code) == 0:
        print("init: Monitor: done")
        logger.info("Monitor: done\n\n"+str(monitor_msg.output))
    else:
        print("init: Monitor: abort\n\n",monitor_msg.output)
        logger.warning("Monitor: abort\n\n"+str(monitor_msg.output))


    with alive_bar(11) as bar:

    # ---------------------------------- FastQC ---------------------------------- #
        
        print("FastQC")
        fastqc = client.containers.get("fastqc")
        fastqc_msg = fastqc.exec_run("fastqc --nogroup --extract --outdir /data/"+dir_pipe+dir_fastqc+" -t "+threads+" "+file1+".fastq "+file2+".fastq" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/", demux=False)
        if int(fastqc_msg.exit_code) == 0:
            print("FastQC: done")
            logger.info("FastQC: done\n\n"+str(fastqc_msg.output))
            bar() 
        else:
            print("FastQC: abort\n\n",fastqc_msg.output)
            logger.warning("FastQC: abort\n\n"+str(fastqc_msg.output))
        
    # -------------------------------- Trimmomatic ------------------------------- #

        print("Trimmomatic")
        trimmomatic = client.containers.get('trimmomatic')
        trimmomatic_comm = "trimmomatic PE "+ file1 +".fastq "+ file2 +".fastq \
            "+ file1 +".trim.fastq.gz "+ file1 +".untrim.fastq.gz \
            "+ file2 +".trim.fastq.gz "+ file2 +".untrim.fastq.gz \
            ILLUMINACLIP:/Trimmomatic-0.39/adapters/NexteraPE-PE.fa:2:40:15 SLIDINGWINDOW:4:20 MINLEN:25 -threads " + threads
        trimmomatic_msg = trimmomatic.exec_run(trimmomatic_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/", demux=False)
        move = os.system("mv -f *.trim* " + dir_scripts+dir_pipe+dir_trimmomatic_trim + " && mv -f *.untrim* " + dir_scripts+dir_pipe+dir_trimmomatic_unpaired)
        if int(trimmomatic_msg.exit_code) == 0:
            print("Trimmomatic: done")
            logger.info("Trimmomatic: done\n\n"+str(trimmomatic_msg.output))
            bar() 
        else:
            print("Trimmomatic: abort\n\n",trimmomatic_msg.output)
            logger.warning("Trimmomatic: abort\n\n"+str(trimmomatic_msg.output))

    # ------------------------------- SPAdes-3.14.1 ------------------------------ #

        print("SPAdes-3.14.1")
        spades = client.containers.get("spades")
        spades_msg = spades.exec_run("python /SPAdes-3.15.4-Linux/bin/rnaspades.py -1 "+ dir_pipe+dir_trimmomatic_trim +"/"+ file1 +".trim.fastq.gz -2 "+ dir_pipe+dir_trimmomatic_trim +"/"+ file2 +".trim.fastq.gz -o "+dir_pipe+dir_spades , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/", demux=False)
        if int(spades_msg.exit_code) == 0:
            print("SPAdes-3.14.1: done")
            logger.info("SPAdes-3.14.1: done\n\n"+str(spades_msg.output))
            bar() 
        else:
            print("SPAdes-3.14.1: abort\n\n",spades_msg.output)
            logger.warning("SPAdes-3.14.1: abort\n\n"+str(spades_msg.output))

    # -------------------------------- CD-HIT-est -------------------------------- #

        print("CD-HIT-est-4.8.1")
        cdhit = client.containers.get('cdhit')
        cdhit_comm = "cd-hit-est -i "+ dir_pipe+dir_spades +"/transcripts.fasta -o "+ dir_pipe+dir_cdhit +"/cd-hit-transcripts.fasta -c 0.9 -d 0 -M 0 -T " + threads
        cdhit_msg=cdhit.exec_run(cdhit_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/in/", demux=False)
        if int(cdhit_msg.exit_code) == 0:
            print("CD-HIT-est-4.8.1: done")
            logger.info("CD-HIT-est-4.8.1: done\n\n"+str(cdhit_msg.output))
            bar() 
        else:
            print("CD-HIT-est-4.8.1: abort\n\n",cdhit_msg.output)
            logger.warning("CD-HIT-est-4.8.1: abort\n\n"+str(cdhit_msg.output))

    # ----------------------------------- BUSCO ---------------------------------- #

        print("BUSCO")
        busco = client.containers.get("busco")
        busco_comm = "busco -i "+ dir_pipe+dir_cdhit +"/cd-hit-transcripts.fasta -o busco_transcripts \
                      --out_path "+ dir_pipe+dir_busco +"/ --download_path "+ dir_pipe+dir_busco +"/busco_downloads -f -c "+ threads +" -m tran --auto-lineage-euk --update-data"
        busco_msg = busco.exec_run(busco_comm , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/busco_wd/", demux=False)
        if int(busco_msg.exit_code) == 0:
            print("BUSCO: done")
            logger.info("BUSCO: done")
            bar() 
        else:
            print("BUSCO: abort\n\n",busco_msg.output)
            logger.warning("BUSCO: abort\n\n"+str(busco_msg.output))

    # ---------------------------------- HISAT2 ---------------------------------- #

        print("HISAT2 - Building indexes")
        hisat = client.containers.get("hisat")   
        hisat_msg = hisat.exec_run("hisat2-build /data/"+dir_pipe+dir_cdhit+"/cd-hit-transcripts.fasta "+pipename+"_index" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_pipe+dir_hisat, demux=False)
        if int(hisat_msg.exit_code) == 0:
            print("HISAT2 - Building indexes: done")
            logger.info("HISAT2 - Building indexes: done")
            bar() 
        else:
            print("HISAT2 - Building indexes: abort\n\n",hisat_msg.output)
            logger.warning("HISAT2 - Building indexes: abort\n\n"+str(hisat_msg.output))
        
    # ---------------------------------- HISAT2 ---------------------------------- #

        print("HISAT2 - Building SAM file")
        hisat_comm="hisat2 -p "+threads+" --dta -q -x /data/"+dir_pipe+dir_hisat+"/"+pipename+"_index \
                    -1 /data/"+dir_pipe+dir_trimmomatic_trim+"/"+file1+".trim.fastq.gz \
                    -2 /data/"+dir_pipe+dir_trimmomatic_trim+"/"+file2+".trim.fastq.gz \
                    -U /data/"+dir_pipe+dir_trimmomatic_unpaired+"/"+file1+".untrim.fastq.gz \
                    -U /data/"+dir_pipe+dir_trimmomatic_unpaired+"/"+file2+".untrim.fastq.gz \
                    -S /data/"+dir_pipe+pipename+".sam"
        hisat_msg = hisat.exec_run(hisat_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_pipe+dir_hisat, demux=False)
        if int(hisat_msg.exit_code) == 0:
            print("HISAT2 - Building SAM file: done")
            logger.info("HISAT2 - Building SAM file: done")
            bar() 
        else:
            print("HISAT2 - Building SAM file: abort\n\n",hisat_msg.output)
            logger.warning("HISAT2 - Building SAM file: abort\n\n"+str(hisat_msg.output))
        
    # ---------------------------------- HISAT2 ---------------------------------- #
        
        print("Samtools - Converting SAM to BAM")
        hisat_msg = hisat.exec_run("samtools sort -@ "+ threads +" -o /data/"+ dir_pipe+pipename +".bam /data/"+ dir_pipe+pipename +".sam", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_pipe+dir_hisat, demux=False)
        if int(hisat_msg.exit_code) == 0:
            print("Samtools - Converting SAM to BAM: done")
            logger.info("Samtools - Converting SAM to BAM: done")
            bar() 
        else:
            print("Samtools - Converting SAM to BAM: abort\n\n",hisat_msg.output)
            logger.warning("Samtools - Converting SAM to BAM: abort\n\n"+str(hisat_msg.output))

    # ---------------------------------- Corset ---------------------------------- #

        print("Corset")
        corset = client.containers.get("corset")
        corset_msg = corset.exec_run("corset -f true /compbio/"+dir_pipe+pipename+".bam" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/compbio/"+dir_pipe+dir_corset, demux=False)
        if int(corset_msg.exit_code) == 0:
            print("Corset: done")
            logger.info("Corset: done")
            bar() 
        else:
            print("Corset: abort\n\n",corset_msg.output)
            logger.warning("Corset: abort\n\n"+str(corset_msg.output))
    
    # --------------------------------- BioPython -------------------------------- #

        print("Fetch Cluster")
        biopython = client.containers.get("biopython")
        biopython_msg = biopython.exec_run("python3 /data/fetchClusterSeqs.py -i /data/"+dir_pipe+dir_cdhit+"/cd-hit-transcripts.fasta -t /data/"+dir_pipe+dir_corset+"/counts.txt -o "+pipename+".fasta -c /data/"+dir_pipe+dir_corset+"/clusters.txt" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_pipe, demux=False)
        if int(biopython_msg.exit_code) == 0:
            print("Fetch Cluster: done")
            logger.info("Fetch Cluster: done")
            bar() 
        else:
            print("Fetch Cluster: abort\n\n",biopython_msg.output)
            logger.warning("Fetch Cluster: abort\n\n"+str(biopython_msg.output))

        # Use case
        #./fetchClusterSeqs.py -i Cdhitest/cd-hit-transcripts.fasta -t counts.txt -o contigs_of_interest.fasta -c clusters.txt

    # ------------------------------- TransDecoder ------------------------------- #

        print("TransDecoder")
        transdecoder = client.containers.get('transdecoder')
        transdecoder_msg=transdecoder.exec_run("TransDecoder.LongOrfs -t "+pipename+".fasta", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_pipe, demux=False)
        if int(transdecoder_msg.exit_code) == 0:
            os.system("mv "+dir_scripts+dir_pipe+"*.transdecoder_dir "+dir_scripts+dir_pipe+dir_transdecoder)
            print("TransDecoder: done")
            logger.info("TransDecoder: done")
            bar()    
        else:
            print("TransDecoder: abort\n\n",transdecoder_msg.output)
            logger.warning("TransDecoder: abort\n\n"+str(transdecoder_msg.output))
        

    print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
              "#                               Pipeline Finished                              #\n"+ \
              "# ---------------------------------------------------------------------------- #\n")


# --------------------------------- PID & DIR -------------------------------- #

if checkStatus():
    print("\nCannot start the same process. Already one existing.\n")
    exit()
pid = os.getpid()
filepid = "/opt/pipeline/var/pipeline.pid"
f = open(filepid,"w+")
f.write(str(pid))
f.close()
os.chdir(str(readWorkdir())+"scripts/")

# ------------------------------- SERVICE LOOP ------------------------------- #

while True:  
    if os.path.exists(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt"):
        input = readFile(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt")
        os.remove(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt")
        Pipeline(input[0], input[1], input[2])
    time.sleep(5)
