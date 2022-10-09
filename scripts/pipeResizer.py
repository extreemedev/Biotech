
def resizeFile(file_name_big, file_name_res, records=2800):
    filebig = open(file_name_big,"r")
    fileres = open(file_name_res,"w+")
    for i in range(records*4):
        fileres.write(filebig.readline())
    filebig.close()
    fileres.close()

resizeFile("SRR2589044_1copy.fastq", "SSR1_resize.fastq")
resizeFile("SRR2589044_2copy.fastq", "SSR2_resize.fastq")
        