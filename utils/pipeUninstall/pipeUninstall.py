import os

# ---------------------------------------------------------------------------- #
#                                 PIP UNINSTALL                                #
# ---------------------------------------------------------------------------- #

piptk = os.system("sudo apt-get update && sudo apt-get remove -y python3-pip python3-tk")
#print(piptk)
dockerinst = os.system("sudo pip remove docker")
#print(dockerinst)
alive = os.system("sudo pip remove alive-progress")
#print(alive)

# ---------------------------------------------------------------------------- #
#                                 WORKDIR TREE                                 #
# ---------------------------------------------------------------------------- #

os.system("sudo rm -r /opt/pipeline/")