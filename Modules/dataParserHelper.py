import Modules.colors as colors


def checkModules(sshModuleList,configModuleList):
  modules = []
  actions =["receivedData","sentData","device_Info","GPS_info","mobile_Info"]
  try:
    for module in configModuleList:
      for moduleName in sshModuleList:
        
        if (module['module']==moduleName):
          temp = 0
          for action in actions:
            if(str(action) == str(module['action'])):
              modules.append(module)
              temp = 1
          if(int(temp) == 0):
            print(f"{colors.WARNING}{module['action']}{colors.FAIL} action do not exists{colors.ENDC}")
            return False
  except:
    print(f"{colors.FAIL} File is empty or formatted incorrectly{colors.ENDC}")
    return False

  return modules

def checkDevice(deviceName, devices):
  i = 0
  for device in devices:
      name = deviceName
      if(len(deviceName)>=len(device['device'])):
        name = deviceName[0:len(device['device'])]
      if(device['device']==name):
        return i
      i+=1
  return -1