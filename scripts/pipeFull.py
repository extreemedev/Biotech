import docker, os


client = docker.from_env()
print(client)


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


# ---------------------------------------------------------------------------- #
#                                  Trimmomatic                                 #
# ---------------------------------------------------------------------------- #


trimmomatic = client.containers.get('trimmomatic')
comm = "trimmomatic PE -threads 4 SRR2589044_1.fastq.gz SRR2589044_2.fastq.gz \
    SRR2589044_1.trim.fastq.gz SRR2589044_1.untrim.fastq.gz \
    SRR2589044_2.trim.fastq.gz SRR2589044_2.untrim.fastq.gz \
    ILLUMINACLIP:/Trimmomatic-0.39/adapters/NexteraPE-PE.fa:2:40:15 SLIDINGWINDOW:4:20 MINLEN:25"

msg_trimmomatic = trimmomatic.exec_run(comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, 
 user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_trimmomatic)

move = os.system("mkdir ./Trimmomatic Trimmomatic/trimmed_fastq Trimmomatic/untrimmed_fastq && mv *.trim* Trimmomatic/trimmed_fastq && mv *.untrim* Trimmomatic/untrimmed_fastq")



# ---------------------------------------------------------------------------- #
#                                 SPAdes-3.14.1                                #
# ---------------------------------------------------------------------------- #


spades = client.containers.get("spades")
print(spades)
msg_spades = spades.exec_run("python /SPAdes-3.15.4-Linux/bin/rnaspades.py -1 Trimmomatic/trimmed_fastq/SRR2589044_1.trim.fastq.gz -2 Trimmomatic/trimmed_fastq/SRR2589044_2.trim.fastq.gz -o Spades " , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_spades)



# ---------------------------------------------------------------------------- #
#                                  CD-HIT-est                                  #
# ---------------------------------------------------------------------------- #

cdhit = client.containers.get('cdhit')
msg_cdhit=cdhit.exec_run("cd .", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_cdhit)


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