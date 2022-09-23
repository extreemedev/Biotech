# ---------------------------------------------------------------------------- #
#                                    Easygui                                   #
# ---------------------------------------------------------------------------- #

import easygui

start = easygui.msgbox("Fully automated Pipeline for Assembly Annotation and Building.\n\nPlease press the 'Accept' button to select the starting file of this Pipeline.","Assembly Pipeline","Accept", "pipe_workflow.png")
if (start == "Accept" or start == "pipe_workflow.png"):
    path = easygui.fileopenbox("Seleziona il file","Pipe")

print("\n"+path+"\n")
