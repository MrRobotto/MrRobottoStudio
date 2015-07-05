import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commons import *
from filegenerator import *

def runMrrExporter():
    startTime = time.time()
    args = sys.argv
    name = args[-1]
    if name not in D.objects:
        blenderExe = sys.executable
        cmdBase = blenderExe + " " + D.filepath + " --background --python " + os.path.realpath(__file__) + " -- " 
        executor = Executor()
        for obj in D.objects:
            if obj.type == "MESH" or obj.type == "CAMERA" or obj.type == "LAMP":
                executor.addCmd(cmdBase+obj.name)
        executor.executeAll()
        stopTime = time.time()
        print("Total Elapsed time: ", stopTime - startTime, "ms")
    else:
        #Exporter().export()
        Exporter2(name).export()
        stopTime = time.time()
        print("Elapsed time: ", stopTime - startTime, "ms")
        
if __name__ == "__main__":
    runMrrExporter()