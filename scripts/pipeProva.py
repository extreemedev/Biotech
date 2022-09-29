import time

while True:
    file = open("/home/matt/app/biotech/scripts/prova.txt","a")
    file.write("Questa é una prova!\n")
    file.close()
    time.sleep(5)
    