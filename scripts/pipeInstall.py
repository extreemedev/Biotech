import os

piptk = os.system("sudo apt-get update && sudo apt-get install -y python3-pip chkconfig")
print(piptk)

dockerinst = os.system("sudo pip install docker")
print(dockerinst)

alive = os.system("sudo pip install alive-progress")
print(alive)

