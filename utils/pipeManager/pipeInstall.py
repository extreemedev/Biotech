import os

# ---------------------------------- GET DIR --------------------------------- #

for root,dirs,files in os.walk("."):
    if "pipeInstall.py" in files:
        inst_dir = root.lstrip(".")
os.chdir(os.getcwd()+inst_dir)

# -------------------------------- PIP INSTALL ------------------------------- #

piptk = os.system("sudo apt-get update && sudo apt-get install -y python3-pip")
dockerinst = os.system("sudo pip install docker")
alive = os.system("sudo pip install alive-progress")
util = os.system("sudo pip install psutil")

# ------------------------------- WORKDIR TREE ------------------------------- #

workdir = os.getcwd().rstrip("/pipeManager").rstrip("utils")
if workdir[-1] != "/":
     workdir+="/"

for i in ("/opt/pipeline","/opt/pipeline/bin","/opt/pipeline/etc","/opt/pipeline/var","/opt/pipeline/log","/opt/pipeline/opt","/opt/pipeline/lib"):
     if not os.path.isdir(i):
          mkdir = os.system("sudo mkdir "+i)
          print("Directory "+i+" successfully created") if (int(mkdir) == 0) else print("Something went wrong when creating the directory "+i+" . If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")
mod = os.system("sudo chmod -R 777 /opt/pipeline/")
print("Workdir tree successfully granted") if (int(mod) == 0) else print("Something went wrong when granting permission. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")

# -------------------------------- SET WORKDIR ------------------------------- #

file = open("/opt/pipeline/etc/workdir.config","w+")
file.write(str(workdir))
file.close()

# ------------------------------- PIPE TRANSFER ------------------------------ #

pipefull = os.system("sudo cp "+workdir+"/utils/pipePackage/pipeFull.py /opt/pipeline/bin/pipeFull.py")
print("Pipeline script successfully deployed") if (int(pipefull) == 0) else print("Something went wrong when deploying the script file. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")
pipeext = os.system("sudo cp "+workdir+"/utils/pipePackage/pipeExtensions.py /opt/pipeline/lib/pipeExtensions.py")
print("Pipeline libraries successfully deployed") if (int(pipeext) == 0) else print("Something went wrong when deploying the script file. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")
pipestat = os.system("sudo cp "+workdir+"/utils/pipePackage/pipeStatus.py /opt/pipeline/lib/pipeStatus.py")
print("Pipeline libraries successfully deployed") if (int(pipestat) == 0) else print("Something went wrong when deploying the script file. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")

# ---------------------------------- SERVICE --------------------------------- #

pipeline_service = os.system("sudo cp "+workdir+"/utils/pipeManager/pipeline /etc/init.d/pipeline")
print("Pipeline service successfully copied (Systemd)") if (int(pipeline_service) == 0) else print("Something went wrong when copying the service file. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")
pipeline_service = os.system("sudo chmod 755 /etc/init.d/pipeline")
print("Pipeline service successfully granted") if (int(pipeline_service) == 0) else print("Something went wrong when granting permission. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")

# --------------------------------- SYSTEMCTL -------------------------------- #

pipeline_sysctl = os.system("sudo cp "+workdir+"/utils/pipeManager/pipeline.service /etc/systemd/system/pipeline.service")
print("Pipeline service successfully copied (Systemctl)") if (int(pipeline_service) == 0) else print("Something went wrong when copying the service file. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")
pipeline_sysctl = os.system("sudo chmod 755 /etc/systemd/system/pipeline.service")
print("Pipeline service successfully granted") if (int(pipeline_service) == 0) else print("Something went wrong when granting permission. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")