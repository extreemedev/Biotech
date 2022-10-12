import docker, os
from alive_progress import alive_bar
from pipeExtensions import *
import time

def Pipeline(pipename,file1,file2,threads="16"):

    print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
              "#                                     Pipe                                     #\n"+ \
              "# ---------------------------------------------------------------------------- #\n")

    dir_trimmomatic = "Trimmomatic"
    dir_trimmomatic_trim = "Trimmomatic/trimmed_fastq"
    dir_trimmomatic_unpaired = "Trimmomatic/untrimmed_fastq"
    dir_spades = "Spades"
    dir_cdhit = "Cdhitest"
    dir_busco = "Busco"
    dir_hisat = "Hisat"
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


    with alive_bar(5) as bar:

    # ---------------------------------------------------------------------------- #
    #                                  Trimmomatic                                 #
    # ---------------------------------------------------------------------------- #

        print("Trimmomatic")
        trimmomatic = client.containers.get('trimmomatic')
        trimmomatic_comm = "trimmomatic PE "+ file1 +".fastq "+ file2 +".fastq \
            "+ file1 +".trim.fastq.gz "+ file1 +".untrim.fastq.gz \
            "+ file2 +".trim.fastq.gz "+ file2 +".untrim.fastq.gz \
            ILLUMINACLIP:/Trimmomatic-0.39/adapters/NexteraPE-PE.fa:2:40:15 SLIDINGWINDOW:4:20 MINLEN:25 -threads " + threads
        trimmomatic_msg = trimmomatic.exec_run(trimmomatic_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        createDirs((dir_trimmomatic, dir_trimmomatic_trim, dir_trimmomatic_unpaired))
        move = os.system("mv -f *.trim* " + dir_trimmomatic_trim + " && mv -f *.untrim* " + dir_trimmomatic_unpaired)
        #print(trimmomatic_msg)
        print("Trimmomatic: done"); bar() if int(trimmomatic_msg.exit_code) == 0 else print("Trimmomatic: abort\n\n",trimmomatic_msg.output)
        #bar()


    # ---------------------------------------------------------------------------- #
    #                                 SPAdes-3.14.1                                #
    # ---------------------------------------------------------------------------- #


        print("SPAdes-3.14.1")
        spades = client.containers.get("spades")
        spades_msg = spades.exec_run("python /SPAdes-3.15.4-Linux/bin/rnaspades.py -1 "+ dir_trimmomatic_trim +"/"+ file1 +".trim.fastq.gz -2 "+ dir_trimmomatic_trim +"/"+ file2 +".trim.fastq.gz -o "+dir_spades , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        #print(spades_msg)
        print("SPAdes-3.14.1: done"); bar() if int(spades_msg.exit_code) == 0 else print("SPAdes-3.14.1: abort\n\n",spades_msg.output)
        #bar()



    # ---------------------------------------------------------------------------- #
    #                                  CD-HIT-est                                  #
    # ---------------------------------------------------------------------------- #

        print("CD-HIT-est-4.8.1")
        createDir(dir_cdhit)
        cdhit = client.containers.get('cdhit')
        cdhit_comm = "cd-hit-est -i "+ dir_spades +"/transcripts.fasta -o "+ dir_cdhit +"/cd-hit-transcripts.fasta -c 0.9 -d 0 -M 0 -T " + threads
        cdhit_msg=cdhit.exec_run(cdhit_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/in", demux=False)
        #print(cdhit_msg)
        print("CD-HIT-est-4.8.1: done"); bar() if int(cdhit_msg.exit_code) == 0 else print("CD-HIT-est-4.8.1: abort\n\n",cdhit_msg.output)
        #bar()

    # ---------------------------------------------------------------------------- #
    #                                     BUSCO                                    #
    # ---------------------------------------------------------------------------- #

        print("BUSCO")
        busco = client.containers.get("busco")
        busco_comm = "busco -i "+ dir_cdhit +"/cd-hit-transcripts.fasta -o busco_cd-hit-transcript \
                      --out_path "+ dir_busco +"/ --download_path "+ dir_busco +"/busco_downloads -f -c "+ threads +" -m tran --auto-lineage-euk --update-data"
        busco_msg = busco.exec_run(busco_comm , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        #print(busco_msg)
        print("BUSCO: done"); bar() if int(busco_msg.exit_code) == 0 else print("BUSCO: abort\n\n",busco_msg.output,".\n\n")
        #bar()

    # ---------------------------------------------------------------------------- #
    #                                    HISAT2                                    #
    # ---------------------------------------------------------------------------- #

        print("HISAT2 - Building indexes")
        createDir(dir_hisat)
        hisat = client.containers.get("hisat")   
        hisat_msg = hisat.exec_run("hisat2-build /data/"+dir_cdhit+"/cd-hit-transcripts.fasta "+pipename+"_index" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_hisat, demux=False)
        print("HISAT2 - Building indexes: done"); bar() if int(hisat_msg.exit_code) == 0 else print("HISAT2 - Building indexes: abort\n\n",hisat_msg.output)
        
        print("HISAT2 - Building SAM file")
        hisat_comm="hisat2 -p "+threads+" --dta -q -x /data/"+dir_hisat+"/"+pipename+"_index \
                    -1 /data/"+dir_trimmomatic_trim+"/"+file1+".trim.fastq.gz \
                    -2 /data/"+dir_trimmomatic_trim+"/"+file2+".trim.fastq.gz \
                    -U /data/"+dir_trimmomatic_unpaired+"/"+file1+".untrim.fastq.gz \
                    -U /data/"+dir_trimmomatic_unpaired+"/"+file2+".untrim.fastq.gz \
                    -S /data/"+pipename+".sam"
        hisat_msg = hisat.exec_run(hisat_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_hisat, demux=False)
        print("HISAT2 - Building SAM file: done"); bar() if int(hisat_msg.exit_code) == 0 else print("HISAT2 - Building SAM file: abort\n\n",hisat_msg.output)
        
        print("Samtools - Converting SAM to BAM")
        hisat_msg = hisat.exec_run("samtools index /data/"+pipename+".sam && samtools view -S -b /data/"+pipename+".sam > /data/"+pipename+".bam", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_hisat, demux=False)
        print("Samtools - Converting SAM to BAM: done"); bar() if int(hisat_msg.exit_code) == 0 else print("Samtools - Converting SAM to BAM: abort\n\n",hisat_msg.output)
        print(hisat_msg)
        

    '''
    # ---------------------------------------------------------------------------- #
    #                                    Corset                                    #
    # ---------------------------------------------------------------------------- #

        print("Corset")
        corset = client.containers.get("corset")
        msg_corset = corset.exec_run("corset -g 1,1,1,2,2,2 -n A1,A2,A3,B1,B2,B3 *.bam" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
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


    
    '''

    print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
              "#                                   Pipe Finished                              #\n"+ \
              "# ---------------------------------------------------------------------------- #\n")

    remove = os.system("rm -rf ../utils/pipePackage/__pycache__")

    

# ---------------------------------------------------------------------------- #
#                                   PID e DIR                                  #
# ---------------------------------------------------------------------------- #

pid = os.getpid()
print(pid)
filepid = "/var/run/user/pipeline.pid"
f = open(filepid,"w+")
f.write(str(pid))
f.close()

#wd = open(".pipedir.wd", "r")
#pathwd = wd.readline()
#wd.close()
os.chdir("/home/matt/app/biotech/scripts/")       #<------ Poi passagli pathwd                  


# ---------------------------------------------------------------------------- #
#                                 SERVICE LOOP                                 #
# ---------------------------------------------------------------------------- #


while True:
    
    if os.path.exists(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt"):
        input = readFile(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt")
        os.remove(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt")
        Pipeline(input[0], input[1], input[2])
    time.sleep(5)
