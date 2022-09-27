import os

def createDirs(dir_names):
    for dir in dir_names:
        if not os.path.isdir("./"+dir):
            os.mkdir(dir)

def createDir(dir_name):
    if not os.path.isdir("./"+dir_name):
        os.mkdir(dir_name)