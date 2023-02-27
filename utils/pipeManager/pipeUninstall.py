import os

def readWorkdir():
    file = open("/opt/pipeline/etc/workdir.config","r")
    workdir = file.readline()
    file.close()
    return(workdir)
# ---------------------------- DOCKER COMPOSE DOWN --------------------------- #

os.system("docker compose -f '"+readWorkdir()+"docker/xubuntu-novnc-biotech/docker-compose.yml' down")

# ------------------------------- PIP UNINSTALL ------------------------------ #

piptk = os.system("sudo apt-get update && sudo apt-get remove -y python3-tk")
dockerinst = os.system("sudo pip uninstall docker")
alive = os.system("sudo pip uninstall alive-progress")
util = os.system("sudo pip uninstall psutil")

# ------------------------------- WORKDIR TREE ------------------------------- #

if os.path.exists("/opt/pipeline/"):    
    print("Workdir tree successfully deleted") if os.system("sudo rm -r /opt/pipeline/")!="0" else print("Something went wrong while deleting workdir tree")

# ---------------------------------- SERVICE --------------------------------- #

if os.path.exists("/etc/init.d/pipeline"):
    print("Service file /etc/init.d/pipeline successfully deleted") if os.system("sudo rm /etc/init.d/pipeline")!="0" else print("Something went wrong while deleting service file /etc/init.d/pipeline")

# --------------------------------- SYSTEMCTL -------------------------------- #


if os.path.exists("/etc/systemd/system/pipeline.service"):
    print("Systemctl service /etc/systemd/system/pipeline.service successfully deleted") if os.system("sudo rm /etc/systemd/system/pipeline.service")!="0" else print("Something went wrong while deleting systemctl service /etc/systemd/system/pipeline.service")

# ---------------------------------- IMAGES ---------------------------------- #

# AGGIUNGERE IN PRIMA POSIZIONE NOVNC
for image in ["mattallev/xubuntu-novnc-biotech:1.0","biocontainers/biopython:v1.73dfsg-1-deb-py3_cv1","ezlabgva/busco:v5.4.3_cv1 ","chrishah/cdhit:v4.8.1", "mdiblbiocore/corset:1.0.9", "staphb/fastqc", "nanozoo/hisat2", "staphb/spades", "biocrusoe/transdecoder", "staphb/trimmomatic"]:
    os.system("sudo docker rmi -f "+image)