# ---------------------------------------------------------------------------- #
#                                    Easygui                                   #
# ---------------------------------------------------------------------------- #

import os, easygui


def selectFile():
    path1 = easygui.fileopenbox("Select your first file","Pipe")
    #print(path1)
    if (str(path1) != "None"):
        path2 = easygui.fileopenbox("Select your second file","Pipe")
        #print(path2)
        if (str(path2) == "None"):
            selectFile()
        else:
            name = str()
            while (str(name) == "") or (str(name) == "None"):
                name = easygui.enterbox("Please insert a name:", "Name selection", os.path.basename(path1).rstrip(".gz").rstrip(".fastq").rstrip(".fasta").rstrip("_1"))
                print(name)
            check = easygui.ynbox("Are you sure you want to proceed?", "Final check")
            print(check)
            if (str(check) == "True"):
                file = open(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt","w+")
                file.write(str(name)+"\n")
                file.write(str(path1)+"\n")
                file.write(str(path2)+"\n")
                file.close()



start = easygui.msgbox("Fully automated Pipeline for Assembly Annotation and Building.\n\nPlease press the 'Accept' button to select the starting file of this Pipeline.","Assembly Pipeline","Accept", "pipe_workflow.png")
#print(start)
if (start == "Accept" or start == "pipe_workflow.png"):
    selectFile()
    
