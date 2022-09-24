import os

pathlist = "Trimmomatic", "Spades", "cdhitest"
for i in pathlist:
    if os.path.exists(i):
        remove = os.system("rm -rf ./"+i)
        if (remove==0):
            print("\n"+i+" directory successfully removed!\n")
    else:
        print("\n"+i+" directory have been removed yet.\n")
