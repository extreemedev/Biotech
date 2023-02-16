import os

print("\n")
pathlist = ".Trash-0", "SSRresize", "Trimmomatic", "Spades", "Cdhitest", "Busco", "Hisat", "Transdecoder", "__pycache__"
for i in pathlist:
    if os.path.exists(i):
        remove = os.system("rm -rf ./"+i)
        if (remove==0):
            print("\n"+i+" directory successfully removed!\n")
    else:
        print("\n"+i+" directory has already been removed.\n")
print("\n")