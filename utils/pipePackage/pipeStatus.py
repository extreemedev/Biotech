import psutil

from pipeExtensions import *


def drawStatus():
    if checkStatus():
        title =  "#                             Pipeline Activated                               #"
        status = "#  Pipeline Status: Waiting user file...                                       #"
    else:
        title =  "#                              Pipeline Stopped                                #"
        status = "#  Pipeline Status: Stopped                                                    #"
    line =   "# ---------------------------------------------------------------------------- #"
    empty =  "#                                                                              #"
    pid =    "#  Process Id: "+readPid()+"                                                               "  
    for i in range(len(readPid())):
        pid = pid[:-1]
    pid += " #"
    status_list = [line, title, line, empty, status, empty, pid, empty, line]
    print("\n")
    [print(elem_list) for elem_list in status_list]
    return(checkStatus())


def checkStatus():
    proc_dicts = findProcessIdByName("python")
    for diction in proc_dicts:
        if str(diction.get('pid')) == readPid():
            return True
    writePid("None")
    return False


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects


if __name__ == "__main__":
    drawStatus()
    quit(1)