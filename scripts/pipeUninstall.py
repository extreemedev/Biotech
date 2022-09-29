import os

piptk = os.system("sudo apt-get update && sudo apt-get remove -y python3-pip python3-tk")
print(piptk)

dockerinst = os.system("pip remove docker")
print(dockerinst)

alive = os.system("pip remove alive-progress")
print(alive)