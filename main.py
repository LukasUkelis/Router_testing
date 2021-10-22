import Modules.testingModules as testingModules
from multiprocessing import Process
import signal
import sys
import time
connectionInfo={'address':"192.168.1.1",'username':"root",'port':"22",'password':"Admin123",'modPort':"502"}
test = testingModules.Testing(connectionInfo)

def stop(signal, frame):
    test.stopTesting()

signal.signal(signal.SIGINT, stop)
test.startTesting()



# if __name__ == "__main__":
#     main()