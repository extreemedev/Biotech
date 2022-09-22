import docker, os


client = docker.from_env()
print(client)


# ---------------------------------------------------------------------------- #
#                                    FastQC                                    #
# ---------------------------------------------------------------------------- #

inputfastqc = "./example.fastq.gz"
outputfastqc = "./fastqc/"
fastqc = client.containers.get("fastqc")
print(fastqc)
messaggioqc = fastqc.exec_run("fastqc --nogroup --extract "+ inputfastqc +" -o "+ outputfastqc , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(messaggioqc)

# ---------------------------------------------------------------------------- #
#                                 SPAdes-3.14.1                                #
# ---------------------------------------------------------------------------- #

