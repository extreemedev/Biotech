# ---------------------------------------------------------------------------- #
#                                    Easygui                                   #
# ---------------------------------------------------------------------------- #

import easygui

start = easygui.msgbox("Fully automated Pipeline for Assembly Annotation and Building.\n\nPlease press the 'Accept' button to select the starting file of this Pipeline.","Assembly Pipeline","Accept", "pipe_workflow.png")
if (start == "Accept" or start == "pipe_workflow.png"):
    path1 = easygui.fileopenbox("Seleziona il primo file","Pipe")
    path2 = easygui.fileopenbox("Seleziona il secondo file","Pipe")
file = open(".assembly#pipe#checkcomm38457*63923!0859#200847572^8*7*8572901@**3928*39$439*945805.txt","w+")
file.write(path1+"\n")
file.write(path2+"\n")
file.close()
#print("\n"+path1+"\n")
