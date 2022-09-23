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
#                                 SPAdes-3.14.1                                #
# ---------------------------------------------------------------------------- #
'''
spades = client.containers.get("spades")
print(spades)
msg_spades = spades.exec_run("python /SPAdes-3.15.4-Linux/bin/rnaspades.py" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_spades)
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