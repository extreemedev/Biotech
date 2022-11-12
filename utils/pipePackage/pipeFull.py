import docker, os, sys
sys.path.insert(0, "/opt/pipeline/lib/")
from alive_progress import alive_bar
from pipeExtensions import *
import time
import logging
logger = logging.getLogger(__name__)  
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/opt/pipeline/log/pipeline.log')
formatter = logging.Formatter('%(asctime)s : %(name)s  : %(funcName)s : %(levelname)s : %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def Pipeline(pipename,file1,file2,threads="16"):
    

    print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
              "#                                Pipeline Started                              #\n"+ \
              "# ---------------------------------------------------------------------------- #\n")

    dir_scripts = readWorkdir()+"scripts/"
    dir_pipe = pipename+"/"
    dir_trimmomatic = "Trimmomatic"
    dir_trimmomatic_trim = "Trimmomatic/trimmed_fastq"
    dir_trimmomatic_unpaired = "Trimmomatic/untrimmed_fastq"
    dir_spades = "Spades"
    dir_cdhit = "Cdhitest"
    dir_busco = "Busco"
    dir_hisat = "Hisat"
    dir_corset = "Corset"
    dir_transdecoder = "Transdecoder"
    client = docker.from_env()
    createDir(dir_scripts+dir_pipe)
    createDirs((dir_scripts+dir_pipe+dir_trimmomatic, dir_scripts+dir_pipe+dir_trimmomatic_trim, dir_scripts+dir_pipe+dir_trimmomatic_unpaired))
    createDir(dir_scripts+dir_pipe+dir_cdhit)
    createDir(dir_scripts+dir_pipe+dir_busco)
    createDir(dir_scripts+dir_pipe+dir_hisat)
    createDir(dir_scripts+dir_pipe+dir_corset)
    os.system("sudo chmod -R 777 "+dir_scripts+dir_pipe)

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
    try:
        monitor = client.containers.get("monidor")
        monitor_msg = monitor.exec_run("fastqc", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
        #print(monitor_msg)
        if int(monitor_msg.exit_code) == 0:
            print("Monitor: done")
            logger.info("Monitor: done")
        else:
            print("Monitor: abort\n\n",monitor_msg.output)
            logger.warning("Monitor: abort\n\n",str(monitor_msg.output))
    except:
        print("WARNING")
    



    with alive_bar(10) as bar:

        # ---------------------------------------------------------------------------- #
        #                                  Trimmomatic                                 #
        # ---------------------------------------------------------------------------- #

        print("Trimmomatic")
        trimmomatic = client.containers.get('trimmomatic')
        trimmomatic_comm = "trimmomatic PE "+ file1 +".fastq "+ file2 +".fastq \
            "+ file1 +".trim.fastq.gz "+ file1 +".untrim.fastq.gz \
            "+ file2 +".trim.fastq.gz "+ file2 +".untrim.fastq.gz \
            ILLUMINACLIP:/Trimmomatic-0.39/adapters/NexteraPE-PE.fa:2:40:15 SLIDINGWINDOW:4:20 MINLEN:25 -threads " + threads
        trimmomatic_msg = trimmomatic.exec_run(trimmomatic_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data", demux=False)
        move = os.system("mv -f *.trim* " + dir_scripts+dir_pipe+dir_trimmomatic_trim + " && mv -f *.untrim* " + dir_scripts+dir_pipe+dir_trimmomatic_unpaired)
        #print(trimmomatic_msg)
        if int(trimmomatic_msg.exit_code) == 0:
            print("Trimmomatic: done")
            bar() 
        else: print("Trimmomatic: abort\n\n",trimmomatic_msg.output)
        #bar()


        # ---------------------------------------------------------------------------- #
        #                                 SPAdes-3.14.1                                #
        # ---------------------------------------------------------------------------- #


        print("SPAdes-3.14.1")
        spades = client.containers.get("spades")
        spades_msg = spades.exec_run("python /SPAdes-3.15.4-Linux/bin/rnaspades.py -1 "+ dir_pipe+dir_trimmomatic_trim +"/"+ file1 +".trim.fastq.gz -2 "+ dir_pipe+dir_trimmomatic_trim +"/"+ file2 +".trim.fastq.gz -o "+dir_pipe+dir_spades , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data", demux=False)
        #print(spades_msg)
        if int(spades_msg.exit_code) == 0:
            print("SPAdes-3.14.1: done")
            bar() 
        else: print("SPAdes-3.14.1: abort\n\n",spades_msg.output)
        #bar()



        # ---------------------------------------------------------------------------- #
        #                                  CD-HIT-est                                  #
        # ---------------------------------------------------------------------------- #

        print("CD-HIT-est-4.8.1")
        cdhit = client.containers.get('cdhit')
        cdhit_comm = "cd-hit-est -i "+ dir_pipe+dir_spades +"/transcripts.fasta -o "+ dir_pipe+dir_cdhit +"/cd-hit-transcripts.fasta -c 0.9 -d 0 -M 0 -T " + threads
        cdhit_msg=cdhit.exec_run(cdhit_comm, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/in", demux=False)
        #print(cdhit_msg)
        if int(cdhit_msg.exit_code) == 0:
            print("CD-HIT-est-4.8.1: done")
            bar() 
        else: print("CD-HIT-est-4.8.1: abort\n\n",cdhit_msg.output)
        #bar()

        # ---------------------------------------------------------------------------- #
        #                                     BUSCO                                    #
        # ---------------------------------------------------------------------------- #

        print("BUSCO")
        busco = client.containers.get("busco")
        busco_comm = "busco -i "+ dir_pipe+dir_cdhit +"/cd-hit-transcripts.fasta -o busco_transcripts \
                      --out_path "+ dir_pipe+dir_busco +"/ --download_path "+ dir_pipe+dir_busco +"/busco_downloads -f -c "+ threads +" -m tran --auto-lineage-euk --update-data"
        busco_msg = busco.exec_run(busco_comm , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/busco_wd", demux=False)
        #print(busco_msg)
        if int(busco_msg.exit_code) == 0:
            print("BUSCO: done")
            bar() 
        else: print("BUSCO: abort\n\n",busco_msg.output)
        #bar()

        # ---------------------------------------------------------------------------- #
        #                                    HISAT2                                    #
        # ---------------------------------------------------------------------------- #

        print("HISAT2 - Building indexes")
        hisat = client.containers.get("hisat")   
        hisat_msg = hisat.exec_run("hisat2-build /data/"+dir_pipe+dir_cdhit+"/cd-hit-transcripts.fasta "+pipename+"_index" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_pipe+dir_hisat, demux=False)
        if int(hisat_msg.exit_code) == 0:
            print("HISAT2 - Building indexes: done")
            bar() 
        else: print("HISAT2 - Building indexes: abort\n\n",hisat_msg.output)
        


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
            bar() 
        else: print("HISAT2 - Building SAM file: abort\n\n",hisat_msg.output)
        

        
        print("Samtools - Converting SAM to BAM")
        hisat_msg = hisat.exec_run("samtools sort -@ "+ threads +" -o /data/"+ dir_pipe+pipename +".bam /data/"+ dir_pipe+pipename +".sam", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_pipe+dir_hisat, demux=False)
        if int(hisat_msg.exit_code) == 0:
            print("Samtools - Converting SAM to BAM: done")
            bar() 
        else: print("Samtools - Converting SAM to BAM: abort\n\n",hisat_msg.output)
        

        # ---------------------------------------------------------------------------- #
        #                                    Corset                                    #
        # ---------------------------------------------------------------------------- #

        print("Corset")
        corset = client.containers.get("corset")
        corset_msg = corset.exec_run("corset -f true /compbio/"+dir_pipe+pipename+".bam" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/compbio/"+dir_pipe+dir_corset, demux=False)
        if int(corset_msg.exit_code) == 0:
            print("Corset: done")
            bar() 
        else: print("Corset: abort\n\n",corset_msg.output)
    

        # ---------------------------------------------------------------------------- #
        #                                   Biopython                                  #
        # ---------------------------------------------------------------------------- #

        print("Fetch Cluster")
        biopython = client.containers.get("biopython")
        biopython_msg = biopython.exec_run("python3 /data/fetchClusterSeqs.py -i /data/"+dir_pipe+dir_cdhit+"/cd-hit-transcripts.fasta -t /data/"+dir_pipe+dir_corset+"/counts.txt -o "+pipename+".fasta -c /data/"+dir_pipe+dir_corset+"/clusters.txt" , stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_pipe, demux=False)
        if int(biopython_msg.exit_code) == 0:
            print("Fetch Cluster: done")
            bar() 
        else: print("Fetch Cluster: abort\n\n",biopython_msg.output)

        #./fetchClusterSeqs.py -i Cdhitest/cd-hit-transcripts.fasta -t counts.txt -o contigs_of_interest.fasta -c clusters.txt


        # ---------------------------------------------------------------------------- #
        #                                 Transdecoder                                 #
        # ---------------------------------------------------------------------------- #

        print("Transdecoder")
        transdecoder = client.containers.get('transdecoder')
        transdecoder_msg=transdecoder.exec_run("TransDecoder.LongOrfs -t "+pipename+".fasta", stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir="/data/"+dir_pipe, demux=False)
        if int(transdecoder_msg.exit_code) == 0:
            print("Transdecoder: done")
            bar()
            os.system("mv "+dir_scripts+dir_pipe+"*.transdecoder_dir "+dir_scripts+dir_pipe+dir_transdecoder)
        else: print("Transdecoder: abort\n\n",transdecoder_msg.output)
        

    
    print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
              "#                               Pipeline Finished                              #\n"+ \
              "# ---------------------------------------------------------------------------- #\n")

    #remove = os.system("rm -rf ../utils/pipePackage/__pycache__")

    print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
              "#                         Pipeline Activated (Waiting...)                      #\n"+ \
              "# ---------------------------------------------------------------------------- #\n"+ \
              "#                                                                              #\n"+ \
              "#  Pipeline Status: Waiting user file...                                       #\n"+ \
              "#                                                                              #\n"+ \
              "#  Process Id: "+str(pid)+"                                                           #\n"+ \
              "#                                                                              #\n"+ \
              "# ---------------------------------------------------------------------------- #\n") \



# ---------------------------------------------------------------------------- #
#                                   PID e DIR                                  #
# ---------------------------------------------------------------------------- #

pid = os.getpid()
filepid = "/var/run/user/pipeline.pid"
f = open(filepid,"w+")
f.write(str(pid))
f.close()

print("\n\n# ---------------------------------------------------------------------------- #\n"+ \
          "#                         Pipeline Activated (Waiting...)                      #\n"+ \
          "# ---------------------------------------------------------------------------- #\n"+ \
          "#                                                                              #\n"+ \
          "#  Pipeline Status: Waiting user file...                                       #\n"+ \
          "#                                                                              #\n"+ \
          "#  Process Id: "+str(pid)+"                                                           #\n"+ \
          "#                                                                              #\n"+ \
          "# ---------------------------------------------------------------------------- #\n") \

os.chdir(str(readWorkdir())+"scripts/")

# ---------------------------------------------------------------------------- #
#                                 SERVICE LOOP                                 #
# ---------------------------------------------------------------------------- #

while True:  
    if os.path.exists(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt"):
        input = readFile(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt")
        os.remove(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt")
        Pipeline(input[0], input[1], input[2])
    time.sleep(5)
