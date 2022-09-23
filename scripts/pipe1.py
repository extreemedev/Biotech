import docker

client = docker.from_env()

#

#Trimmomatic
trimmomatic = client.containers.get('trimmomatic')
comm = "trimmomatic PE -threads 4 SRR2589044_1.fastq.gz SRR2589044_2.fastq.gz \
    SRR2589044_1.trim.fastq.gz SRR2589044_1un.trim.fastq.gz \
    SRR2589044_2.trim.fastq.gz SRR2589044_2un.trim.fastq.gz \
    ILLUMINACLIP:/Trimmomatic-0.39/adapters/NexteraPE-PE.fa:2:40:15 SLIDINGWINDOW:4:20 MINLEN:25"
#std_comm = 'java -jar /Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 60 -phred33 BP_87_1.fq.gz BP_87_2.fq.gz \
# BP_87_1.trimmed.paired.fastq BP_87_1.trimmed.unpaired.fastq BP_87_2.trimmed.paired.fastq BP_87_2.trimmed.unpaired.fastq 
# \ ILLUMINACLIP:/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 SLIDINGWINDOW:4:15 MINLEN:36 HEADCROP:13'
msg_trimmomatic = trimmomatic.exec_run(comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, 
 user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_trimmomatic)

#CD-HIT-est
cd_hit_est = client.containers.get('cdhit')
msg_cd_hit_est=cd_hit_est.exec_run("cd .", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_cd_hit_est)

#Detonate
detonate = client.containers.get('detonate')
msg_detonate=detonate.exec_run("cd .", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_detonate)

#Transdecoder
transdecoder = client.containers.get('transdecoder')
msg_transdecoder=transdecoder.exec_run("cd .", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
print(msg_transdecoder)