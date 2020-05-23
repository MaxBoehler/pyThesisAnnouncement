import os
import glob
from shutil import which
import subprocess

def prechecking(file, isFolder):
    absPath = os.getcwd()
    filePath = os.path.join(absPath,file)
    if isFolder:
        if not os.path.isdir(filePath):
            raise FileNotFoundError(file + "/ not found")
        elif file == "tex":
            if not os.path.isdir(os.path.join(filePath, "img")):
                os.mkdir(os.path.join(filePath, "img"))
        elif file != "tex":
            files = []
            for f in glob.glob(os.path.join(filePath,"*")):
                files.append(f)
            if files == []:
                raise FileNotFoundError("No files in folder " + file + "/")
    else:
        if not os.path.isfile(filePath):
            raise FileNotFoundError(file + "/ not found")

def checkExecutable(exe):
    check = which(exe)
    if check == None:
        raise ImportError(exe + " command not found on your system. Please install " + exe + ".")

def shellCommand(dir, command):
    proc = subprocess.Popen(command.split(" "), cwd=dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        if err == b"":
            raise Exception(out.decode("utf-8"))
        else:
            raise Exception(err.decode("utf-8"))




def calcMask(x2,x1,y2,y1,b,x):
    m = (y2-y1) / (x2-x1)
    return m * x + b
