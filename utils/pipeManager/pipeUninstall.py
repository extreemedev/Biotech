import os

# ------------------------------- PIP UNINSTALL ------------------------------ #

piptk = os.system("sudo apt-get update && sudo apt-get remove -y python3-tk")
dockerinst = os.system("sudo pip remove docker")
alive = os.system("sudo pip remove alive-progress")
util = os.system("sudo pip remove psutil")

# ------------------------------- WORKDIR TREE ------------------------------- #

os.system("sudo rm -r /opt/pipeline/")

# ---------------------------------- SERVICE --------------------------------- #

pipeline_service = os.system("sudo rm /etc/init.d/pipeline")

# --------------------------------- SYSTEMCTL -------------------------------- #

#if il file esiste, allora rimuovilo
pipeline_sysctl = os.system("sudo rm /etc/systemd/system/pipeline.service") #Mettere in console la disinstallazione andata a buon fine