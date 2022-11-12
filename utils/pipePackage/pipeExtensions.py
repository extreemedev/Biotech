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
