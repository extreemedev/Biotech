import os

piptk = os.system("sudo apt-get update && sudo apt-get install -y python3-pip python3-tk cron")
print(piptk)

dockerinst = os.system("pip install docker")
print(dockerinst)

alive = os.system("pip install alive-progress")
print(alive)