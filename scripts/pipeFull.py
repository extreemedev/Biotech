import docker, os
from alive_progress import alive_bar
import time



def createDirs(dir_names):
    for dir in dir_names:
        if not os.path.isdir("./"+dir):
            os.mkdir(dir)

def createDir(dir_name):
    if not os.path.isdir("./"+dir_name):
        os.mkdir(dir_name)



print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
          "#                                     Pipe                                     #\n"+ \
          "# ---------------------------------------------------------------------------- #\n")


client = docker.from_env()


# ---------------------------------------------------------------------------- #
#                                    FastQC                                    #
# ---------------------------------------------------------------------------- #
'''
infastqc = "./example.fastq.gz"
outfastqc = "./fastqc/"
fastqc = client.containers.get("fastqc")
print(fastqc)
msg_fastqc = fastqc.exec_run("fastqc --nogroup --extract "+ infastqc +" -o "+ outfastqc , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_fastqc)
'''





with alive_bar(3) as bar:

# ---------------------------------------------------------------------------- #
#                                  Trimmomatic                                 #
# ---------------------------------------------------------------------------- #

    print("Trimmomatic")
    trimmomatic = client.containers.get('trimmomatic')
    comm = "trimmomatic PE -threads 4 SRR2589044_1.fastq.gz SRR2589044_2.fastq.gz \
        SRR2589044_1.trim.fastq.gz SRR2589044_1.untrim.fastq.gz \
        SRR2589044_2.trim.fastq.gz SRR2589044_2.untrim.fastq.gz \
        ILLUMINACLIP:/Trimmomatic-0.39/adapters/NexteraPE-PE.fa:2:40:15 SLIDINGWINDOW:4:20 MINLEN:25"
    msg_trimmomatic = trimmomatic.exec_run(comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, 
        user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
    #print(msg_trimmomatic)
    createDirs(("Trimmomatic", "Trimmomatic/trimmed_fastq", "Trimmomatic/untrimmed_fastq"))
    move = os.system("mv -f *.trim* Trimmomatic/trimmed_fastq && mv -f *.untrim* Trimmomatic/untrimmed_fastq")
    print("Trimmomatic: done")
    bar()


# ---------------------------------------------------------------------------- #
#                                 SPAdes-3.14.1                                #
# ---------------------------------------------------------------------------- #


    print("SPAdes-3.14.1")
    spades = client.containers.get("spades")
    msg_spades = spades.exec_run("python /SPAdes-3.15.4-Linux/bin/rnaspades.py -1 Trimmomatic/trimmed_fastq/SRR2589044_1.trim.fastq.gz -2 Trimmomatic/trimmed_fastq/SRR2589044_2.trim.fastq.gz -o Spades " , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
    #print(msg_spades)
    print("SPAdes-3.14.1: done")
    bar()



# ---------------------------------------------------------------------------- #
#                                  CD-HIT-est                                  #
# ---------------------------------------------------------------------------- #


    cdhit = client.containers.get('cdhit')
    cdhit_comm = "cd-hit-est -i example.fastq -o cd-hit-transcripts -c 0.9 -d 0 -M 0 -T 16"
    msg_cdhit=cdhit.exec_run(cdhit_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/in", demux=False)
    print(msg_cdhit)
    createDir("cdhitest")
    move = os.system("mv -f *cd-hit-transcripts /cdhitest")
    bar()

'''
# ---------------------------------------------------------------------------- #
#                                     busco                                    #
# ---------------------------------------------------------------------------- #

busco = client.containers.get("busco")
print(busco)
msg_busco = busco.exec_run("" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_busco)


# ---------------------------------------------------------------------------- #
#                                    Corset                                    #
# ---------------------------------------------------------------------------- #

corset = client.containers.get("corset")
print(corset)
msg_corset = corset.exec_run("" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_corset)


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