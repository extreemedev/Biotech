import docker, os
from alive_progress import alive_bar
from pipeExtensions import *
import time

def Pipeline(file1,file2,threads="16"):

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

    print("Monitor")
    monitor = client.containers.get("monitor")
    monitor_msg = monitor.exec_run("fastqc", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
    #print(monitor_msg)
    print("Monitor: done") if int(monitor_msg.exit_code) == 0 else print("Monitor: abort\n\n",monitor_msg.output)


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
        print("Trimmomatic: done"); bar() if int(trimmomatic_msg.exit_code) == 0 else print("Trimmomatic: abort\n\n",trimmomatic_msg.output)
        #bar()


    # ---------------------------------------------------------------------------- #
    #                                 SPAdes-3.14.1                                #
    # ---------------------------------------------------------------------------- #


        print("SPAdes-3.14.1")
        spades = client.containers.get("spades")
        spades_msg = spades.exec_run("python /SPAdes-3.15.4-Linux/bin/rnaspades.py -1 Trimmomatic/trimmed_fastq/"+ file1 +".trim.fastq.gz -2 Trimmomatic/trimmed_fastq/"+ file2 +".trim.fastq.gz -o Spades " , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        #print(spades_msg)
        print("SPAdes-3.14.1: done"); bar() if int(spades_msg.exit_code) == 0 else print("SPAdes-3.14.1: abort\n\n",spades_msg.output)
        #bar()



    # ---------------------------------------------------------------------------- #
    #                                  CD-HIT-est                                  #
    # ---------------------------------------------------------------------------- #
        var = "Spades/transcripts.fasta"
        print("CD-HIT-est-4.8.1")
        cdhit = client.containers.get('cdhit')
        createDir("cdhitest")
        cdhit_comm = "cd-hit-est -i example.fasta -o cdhitest/cd-hit-transcripts.fasta -c 0.9 -d 0 -M 0 -T " + threads
        cdhit_msg=cdhit.exec_run(cdhit_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/in", demux=False)
        #print(cdhit_msg)
        print("CD-HIT-est-4.8.1: done"); bar() if int(cdhit_msg.exit_code) == 0 else print("CD-HIT-est-4.8.1: abort\n\n",cdhit_msg.output)
        #bar()

    # ---------------------------------------------------------------------------- #
    #                                     busco                                    #
    # ---------------------------------------------------------------------------- #

        print("busco")
        busco = client.containers.get("busco")
        busco_comm = "busco -i cdhitest/cd-hit-transcripts.fasta -o busco_cd-hit-transcript \
                      --out_path busco/ --download_path busco/busco_downloads -f -c "+ threads +" -m tran --auto-lineage-euk --update-data"
        busco_msg = busco.exec_run(busco_comm , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        #print(busco_msg)
        print("busco: done"); bar() if int(busco_msg.exit_code) == 0 else print("busco: abort\n\n",busco_msg.output)
        #bar()

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

# ---------------------------------------------------------------------------- #
#                                     START                                    #
# ---------------------------------------------------------------------------- #
    
pid = os.getpid()
print(pid)
filepid = "/var/run/user/pipeline.pid"
f = open(filepid,"w+")
f.write(str(pid))
f.close()

while True:
    if os.path.exists(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt"):
        input = readFile(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt")
        os.remove(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt")
        Pipeline(input[0], input[1])
    time.sleep(5)
