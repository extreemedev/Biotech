import os

pip = os.system("sudo apt update && sudo apt install -y python3-pip")
print(pip)

dockerinst = os.system("pip install docker")
print(dockerinst)
# You could also use the os.popen() method
#with os.popen("ls -lh") as f:
    #print(f.readlines())
