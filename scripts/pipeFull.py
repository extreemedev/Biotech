import docker, os
from alive_progress import alive_bar
from mkdir import *
import time

def Pipeline(file1,file2,threads):

    print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
              "#                                     Pipe                                     #\n"+ \
              "# ---------------------------------------------------------------------------- #\n")

    client = docker.from_env()

    # ---------------------------------------------------------------------------- #
    #                                    FastQC                                    #
    # ---------------------------------------------------------------------------- #
    '''
    print("FastQC")
    fastqc_in = file1
    fastqc_out = "./fastqc/"
    fastqc = client.containers.get("fastqc")
    fastqc_msg = fastqc.exec_run("fastqc --nogroup --extract "+ fastqc_in +" -o "+ fastqc_out , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
    print(fastqc_msg)
    '''

    monitor = client.containers.get("monitor")
    print("Monitor")
    monitor_msg = monitor.exec_run("fastqc", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
    print(monitor_msg)

    with alive_bar(4) as bar:

    # ---------------------------------------------------------------------------- #
    #                                  Trimmomatic                                 #
    # ---------------------------------------------------------------------------- #

        print("Trimmomatic")
        trimmomatic = client.containers.get('trimmomatic')
        trimmomatic_comm = "trimmomatic PE "+ file1 +".fastq.gz "+ file2 +".fastq.gz \
            "+ file1 +".trim.fastq.gz "+ file1 +".untrim.fastq.gz \
            "+ file2 +".trim.fastq.gz "+ file2 +".untrim.fastq.gz \
            ILLUMINACLIP:/Trimmomatic-0.39/adapters/NexteraPE-PE.fa:2:40:15 SLIDINGWINDOW:4:20 MINLEN:25 -threads " + threads
        trimmomatic_msg = trimmomatic.exec_run(trimmomatic_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        #print(trimmomatic_msg)
        createDirs(("Trimmomatic", "Trimmomatic/trimmed_fastq", "Trimmomatic/untrimmed_fastq"))
        move = os.system("mv -f *.trim* Trimmomatic/trimmed_fastq && mv -f *.untrim* Trimmomatic/untrimmed_fastq")
        print("Trimmomatic: done")
        bar()


    # ---------------------------------------------------------------------------- #
    #                                 SPAdes-3.14.1                                #
    # ---------------------------------------------------------------------------- #


        print("SPAdes-3.14.1")
        spades = client.containers.get("spades")
        spades_msg = spades.exec_run("python /SPAdes-3.15.4-Linux/bin/rnaspades.py -1 Trimmomatic/trimmed_fastq/"+ file1 +".trim.fastq.gz -2 Trimmomatic/trimmed_fastq/"+ file2 +".trim.fastq.gz -o Spades " , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        print(spades_msg)
        print("SPAdes-3.14.1: done")
        bar()



    # ---------------------------------------------------------------------------- #
    #                                  CD-HIT-est                                  #
    # ---------------------------------------------------------------------------- #
        var = "Spades/transcripts.fasta"
        print("CD-HIT-est-4.8.1")
        cdhit = client.containers.get('cdhit')
        createDir("cdhitest")
        cdhit_comm = "cd-hit-est -i example.fasta -o cdhitest/cd-hit-transcripts.fasta -c 0.9 -d 0 -M 0 -T " + threads
        cdhit_msg=cdhit.exec_run(cdhit_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/in", demux=False)
        print(cdhit_msg)
        bar()


    # ---------------------------------------------------------------------------- #
    #                                     busco                                    #
    # ---------------------------------------------------------------------------- #

        print("busco")
        busco = client.containers.get("busco")
        busco_comm = "busco -i cdhitest/cd-hit-transcripts.fasta -o busco_cd-hit-transcript \
                      --out_path busco/ --download_path busco/busco_downloads -f -c "+ threads +" -m tran --auto-lineage-euk --update-data"
        busco_msg = busco.exec_run(busco_comm , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        print(busco_msg)
        bar()

    '''
    # ---------------------------------------------------------------------------- #
    #                                    Corset                                    #
    # ---------------------------------------------------------------------------- #

        print("Corset")
        corset = client.containers.get("corset")
        msg_corset = corset.exec_run("corset" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        print(msg_corset)
        bar()


    # ---------------------------------------------------------------------------- #
    #                                   Detonate                                   #
    # ---------------------------------------------------------------------------- #


        detonate = client.containers.get('detonate')
        msg_detonate=detonate.exec_run("cd .", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        print(msg_detonate)


    # ---------------------------------------------------------------------------- #
    #                                 Transdecoder                                 #
    # ---------------------------------------------------------------------------- #


        transdecoder = client.containers.get('transdecoder')
        msg_transdecoder=transdecoder.exec_run("cd .", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        print(msg_transdecoder)


    # ---------------------------------------------------------------------------- #
    #                            SOAPdenovo-Trans-1.0.4                            #
    # ---------------------------------------------------------------------------- #

        soapdenovo = client.containers.get("soapdenovo")
        print(soapdenovo)
        msg_soap = soapdenovo.exec_run("" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        print(msg_soap)


    # ---------------------------------------------------------------------------- #
    #                                 salmon-1.5.1                                 #
    # ---------------------------------------------------------------------------- #


        salmon = client.containers.get("salmon")
        print(salmon)
        msg_salmon = salmon.exec_run("" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        print(msg_salmon)


    # ---------------------------------------------------------------------------- #
    #                                    HISAT2                                    #
    # ---------------------------------------------------------------------------- #

        hisat = client.containers.get("hisat")
        print(hisat)
        msg_hisat = hisat.exec_run("" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        print(msg_hisat)
    '''
    remove = os.system("rm -rf __pycache__")

Pipeline("SRR2589044_1", "SRR2589044_2", "16")