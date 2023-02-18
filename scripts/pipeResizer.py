import os
os.chdir("/home/headless/Desktop/Biotech")

def resizeFile(file_name_big, file_name_res, records=2800):
    filebig = open(file_name_big,"r")
    fileres = open(file_name_res,"w+")
    for i in range(records*4):
        fileres.write(filebig.readline())
    filebig.close()
    fileres.close()

resizeFile("SRR2589044_1.fastq", "SSRresize_1.fastq")
resizeFile("SRR2589044_2.fastq", "SSRresize_2.fastq")
        