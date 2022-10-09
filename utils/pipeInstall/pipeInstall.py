import os

piptk = os.system("sudo apt-get update && sudo apt-get install -y python3-pip chkconfig")
#print(piptk)
dockerinst = os.system("sudo pip install docker")
#print(dockerinst)
alive = os.system("sudo pip install alive-progress")
#print(alive)

pipeline = os.system("sudo cp /home/matt/app/biotech/utils/pipeInstall/pipeline /etc/init.d/pipeline")
print("\n\nPipeline service successfully copied!\n") if (int(pipeline) == 0) else print("Something went wrong when copying the service file.")

home = os.system("$HOME")
print(home)