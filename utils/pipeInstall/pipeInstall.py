import os

# ---------------------------------------------------------------------------- #
#                                 PIP INSTALLS                                 #
# ---------------------------------------------------------------------------- #

piptk = os.system("sudo apt-get update && sudo apt-get install -y python3-pip chkconfig")
dockerinst = os.system("sudo pip install docker")
alive = os.system("sudo pip install alive-progress")
biopython = os.system("sudo pip install biopython")

# ---------------------------------------------------------------------------- #
#                                 WORKDIR TREE                                 #
# ---------------------------------------------------------------------------- #

workdir = os.getcwd().rstrip("/pipeInstall").rstrip("utils")

"""
/opt/
  ├─ pipeline/
        ├─ bin/
        ├─ etc/
        ├─ lib/
        ├─ log/
        ├─ opt/
        ├─ var/
"""
for i in ("/opt/pipeline","/opt/pipeline/bin","/opt/pipeline/etc","/opt/pipeline/var","/opt/pipeline/log","/opt/pipeline/opt","/opt/pipeline/lib"):
     if not os.path.isdir(i):
          mkdir = os.system("sudo mkdir "+i)
          print("\nDirectory successfully created!\n") if (int(mkdir) == 0) else print("Something went wrong when creating the directory. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")
mod = os.system("sudo chmod -R 777 /opt/pipeline/")
print("Workdir tree successfully granted.") if (int(mod) == 0) else print("Something went wrong when granting permission. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")

file = open("/opt/pipeline/etc/workdir.config","w+")
file.write(str(workdir))
file.close()

pipefull = os.system("sudo cp "+workdir+"utils/pipePackage/pipeFull.py /opt/pipeline/bin/pipeFull.py")
print("Pipeline script successfully deployed.") if (int(pipefull) == 0) else print("Something went wrong when deploying the script file. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")
pipext = os.system("sudo cp "+workdir+"utils/pipePackage/pipeExtensions.py /opt/pipeline/lib/pipeExtensions.py")
print("Pipeline libraries successfully deployed.") if (int(pipext) == 0) else print("Something went wrong when deploying the script file. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")


pipeline_service = os.system("sudo cp "+workdir+"utils/pipeInstall/pipeline /etc/init.d/pipeline")
print("Pipeline service successfully copied.") if (int(pipeline_service) == 0) else print("Something went wrong when copying the service file. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")
pipeline_service = os.system("sudo chmod 755 /etc/init.d/pipeline")
print("Pipeline service successfully granted.") if (int(pipeline_service) == 0) else print("Something went wrong when granting permission. If the problem persists please read the documentation here: https://github.com/extreemedev/Biotech/blob/master/README.md\n")