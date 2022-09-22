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
msgfastqc = fastqc.exec_run("fastqc --nogroup --extract "+ infastqc +" -o "+ outfastqc , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msgfastqc)
'''
# ---------------------------------------------------------------------------- #
#                                 SPAdes-3.14.1                                #
# ---------------------------------------------------------------------------- #

inspades = "./example.fastq.gz"
outspades = "./fastqc/"
spades = client.containers.get("spades")
print(spades)
msgspades = spades.exec_run("python /SPAdes-3.15.4-Linux/bin/rnaspades.py" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msgspades)
