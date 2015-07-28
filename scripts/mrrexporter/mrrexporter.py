import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commons import *
from filegenerator import *

def runMrrExporter():
    startTime = time.time()
    args = sys.argv
    filenameBase = os.path.splitext(D.filepath)[0]
    filename = filenameBase + ".mrr"
    Exporter(filename).export()
    stopTime = time.time()
    print("Elapsed time: ", stopTime - startTime, "s")

def runMrrExporter2():
    startTime = time.time()
    args = sys.argv
    name = args[-1]
    filenameBase = os.path.splitext(D.filepath)[0]
    if name not in D.objects:
        blenderExe = sys.executable
        cmdBase = blenderExe + " " + D.filepath + " --background --python " + os.path.realpath(__file__) + " -- " 
        executor = Executor()
        joiner = Joiner()
        for obj in D.objects:
            if obj.type == "MESH" or obj.type == "CAMERA" or obj.type == "LAMP":
                executor.addCmd(cmdBase+obj.name)
                joiner.addFileToJoin(filenameBase + "_" + name + ".mrr", obj.type)
        executor.executeAll()
        stopTime = time.time()
        print("Total Elapsed time: ", stopTime - startTime, "s")
    else:
        #Exporter().export()
        nameCleaned = cleanName(name)
        filename = filenameBase + "_" + nameCleaned + ".mrr"
        Exporter2(name, filename).export()
        stopTime = time.time()
        print("Elapsed time: ", stopTime - startTime, "s")
        
if __name__ == "__main__":
    runMrrExporter()