import os

def createDirs(dir_names):
    for dir in dir_names:
        if not os.path.isdir("./"+dir):
            os.mkdir(dir)
