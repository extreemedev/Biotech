import os

def createDirs(dir_paths):
    for dir in dir_paths:
        createDir(dir)


def createDir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def readFile(file_name):
    file = open(file_name,"r")
    pipename = file.readline().strip("\n")
    string1 = file.readline().split("/")
    string2 = file.readline().split("/")
    for word in string1:
        if word.endswith("\n"):
            file1 = word.strip("\n").rstrip("gz").rstrip(".").rstrip("fastq").rstrip("fasta").rstrip(".")
    for word in string2:
        if word.endswith("\n"):
            file2 = word.strip("\n").rstrip("gz").rstrip(".").rstrip("fastq").rstrip("fasta").rstrip(".")
    file.close()
    return(pipename, file1, file2)


def readWorkdir():
    file = open("/opt/pipeline/etc/workdir.config","r")
    workdir = file.readline()
    file.close()
    return(workdir)


def readPid():
    filepid = "/opt/pipeline/var/pipeline.pid"
    if os.path.isfile(filepid):
        f = open(filepid,"r")
        pid = str(f.readline())
        f.close()
        return(pid)
    else:
        return(None)


def writePid(string):
    filepid = "/opt/pipeline/var/pipeline.pid"
    f = open(filepid,"w+")
    f.write(string)
    f.close()


def cleanLog(string):
    string_proc = string.lstrip("b")
    for i in range(len(string_proc)):
        if string_proc[i]=="t" and string_proc[i-1]=="\\":
            string_proc[i].replace("t","    ")
            string_proc[i-1].replace("\\","")
    return(string_proc)
    pass


#busco_log = str(b"2022-11-15 11:56:33 INFO:\t***** Start a BUSCO v5.4.3 analysis, current time: 11/15/2022 11:56:33 *****\n2022-11-15 11:56:33 INFO:\tConfiguring BUSCO with local environment\n2022-11-15 11:56:33 INFO:\tMode is transcriptome\n2022-11-15 11:56:33 INFO:\tDownloading information on latest versions of BUSCO data...\n2022-11-15 11:56:36 INFO:\tInput file is /busco_wd/SSRresize/Cdhitest/cd-hit-transcripts.fasta\n2022-11-15 11:56:36 INFO:\tNo lineage specified. Running lineage auto selector.\n\n2022-11-15 11:56:36 INFO:\t***** Starting Auto Select Lineage *****\n\tThis process runs BUSCO on the generic lineage datasets for the domains archaea, bacteria and eukaryota. Once the optimal domain is selected, BUSCO automatically attempts to find the most appropriate BUSCO dataset to use based on phylogenetic placement.\n\t--auto-lineage-euk and --auto-lineage-prok are also available if you know your input assembly is, or is not, an eukaryote. See the user guide for more information.\n\tA reminder: Busco evaluations are valid when an appropriate dataset is used, i.e., the dataset belongs to the lineage of the species to test. Because of overlapping markers/spurious matches among domains, busco matches in another domain do not necessarily mean that your genome/proteome contains sequences from this domain. However, a high busco score in multiple domains might help you identify possible contaminations.\n2022-11-15 11:56:36 INFO:\tDownloading file 'https://busco-data.ezlab.org/v5/data/lineages/eukaryota_odb10.2020-09-10.tar.gz'\n2022-11-15 11:56:45 INFO:\tDecompressing file '/busco_wd/SSRresize/Busco/busco_downloads/lineages/eukaryota_odb10.tar.gz'\n2022-11-15 11:56:47 INFO:\tRunning BUSCO using lineage dataset eukaryota_odb10 (eukaryota, 2020-09-10)\n2022-11-15 11:56:49 INFO:\tRunning 1 job(s) on metaeuk, starting at 11/15/2022 11:56:49\n2022-11-15 11:56:57 INFO:\t[metaeuk]\t1 of 1 task(s) completed\n2022-11-15 11:56:57 INFO:\t***** Run HMMER on gene sequences *****\n2022-11-15 11:56:57 INFO:\tRunning 255 job(s) on hmmsearch, starting at 11/15/2022 11:56:57\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t26 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t51 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t51 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t51 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t77 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t102 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t102 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t128 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t128 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t153 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t153 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t204 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t230 of 255 task(s) completed\n2022-11-15 11:56:58 INFO:\t[hmmsearch]\t255 of 255 task(s) completed\n2022-11-15 11:56:58 WARNING:\tBUSCO did not find any match. Make sure to check the log files if this is unexpected.\n2022-11-15 11:56:58 INFO:\tResults:\tC:0.0%[S:0.0%,D:0.0%],F:0.0%,M:100.0%,n:255\t   \n\n2022-11-15 11:56:58 INFO:\tExtracting missing and fragmented buscos from the file refseq_db.faa...\n2022-11-15 11:57:08 INFO:\tRunning 1 job(s) on metaeuk, starting at 11/15/2022 11:57:08\n2022-11-15 11:57:16 INFO:\t[metaeuk]\t1 of 1 task(s) completed\n2022-11-15 11:57:16 INFO:\t***** Run HMMER on gene sequences *****\n2022-11-15 11:57:16 INFO:\tRunning 255 job(s) on hmmsearch, starting at 11/15/2022 11:57:16\n2022-11-15 11:57:17 INFO:\t[hmmsearch]\t26 of 255 task(s) completed\n2022-11-15 11:57:17 INFO:\t[hmmsearch]\t51 of 255 task(s) completed\n2022-11-15 11:57:17 INFO:\t[hmmsearch]\t77 of 255 task(s) completed\n2022-11-15 11:57:17 INFO:\t[hmmsearch]\t128 of 255 task(s) completed\n2022-11-15 11:57:17 INFO:\t[hmmsearch]\t153 of 255 task(s) completed\n2022-11-15 11:57:17 INFO:\t[hmmsearch]\t179 of 255 task(s) completed\n2022-11-15 11:57:17 INFO:\t[hmmsearch]\t204 of 255 task(s) completed\n2022-11-15 11:57:17 INFO:\t[hmmsearch]\t230 of 255 task(s) completed\n2022-11-15 11:57:17 INFO:\t[hmmsearch]\t255 of 255 task(s) completed\n2022-11-15 11:57:17 WARNING:\tBUSCO did not find any match. Make sure to check the log files if this is unexpected.\n2022-11-15 11:57:17 INFO:\tResults:\tC:0.0%[S:0.0%,D:0.0%],F:0.0%,M:100.0%,n:255\t   \n\n2022-11-15 11:57:17 ERROR:\tNo genes were recognized by BUSCO. Please check the content of your input file.\n2022-11-15 11:57:17 ERROR:\tBUSCO analysis failed!\n2022-11-15 11:57:17 ERROR:\tCheck the logs, read the user guide (https://busco.ezlab.org/busco_userguide.html), and check the BUSCO issue board on https://gitlab.com/ezlab/busco/issues\n\n")
#print("\n"+cleanLog(busco_log)+"\n")