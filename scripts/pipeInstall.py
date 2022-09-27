import os

pip = os.system("sudo apt update && sudo apt install -y python3-pip")
print(pip)

tk = os.system("sudo apt-get update && sudo apt-get install -y python3-tk")
print(tk)

dockerinst = os.system("pip install docker")
print(dockerinst)

alive = os.system("pip install alive-progress")
print(alive)