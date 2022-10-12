import os

def createDirs(dir_names):
    for dir in dir_names:
        if not os.path.isdir("./"+dir):
            os.mkdir(dir)

def createDir(dir_name):
    if not os.path.isdir("./"+dir_name):
        os.mkdir(dir_name)

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

def setWorkdir(dir_name):
    shell_name = str(os.system("find $HOME -name "+dir_name+" -exec echo {}"))
    print(shell_name)
    if ("/" in str(shell_name[0])):
        print("OK")
        file = open(".pipedir.wd","w+")
        file.write(str(dir_name))
        file.close()