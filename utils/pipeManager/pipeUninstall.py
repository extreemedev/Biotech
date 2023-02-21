import os

# ------------------------------- PIP UNINSTALL ------------------------------ #

piptk = os.system("sudo apt-get update && sudo apt-get remove -y python3-tk")
dockerinst = os.system("sudo pip remove docker")
alive = os.system("sudo pip remove alive-progress")

# ------------------------------- WORKDIR TREE ------------------------------- #

os.system("sudo rm -r /opt/pipeline/")