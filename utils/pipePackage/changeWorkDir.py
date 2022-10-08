import os
from pipeExtensions import *

print("Are you sure you want to change your pipeline working directory?[y/N] ")
sure = input()
if (sure == "y") or (sure == "Y"):
    print("Please, type an existing directory: ")
    dir_name = input()
    if (dir_name == ""):
        print("Invalid text argument. Working directory not changed.")
    else:
        setWorkdir(dir_name)
else:
    print("Working directory not changed.")