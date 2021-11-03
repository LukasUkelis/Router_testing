import json
import Modules.colors as colors

class Data:
  
  __data = None
  __dataPath  = 'data2.json'
  __deviceID = -1
  __targets = 0

  def __init__(self):
      pass

  def openJson(self,deviceName):
    try:
      self.file = open(self.__dataPath)
      self.__data = json.load(self.file)
      self.file.close()
    except:
      print(f"{colors.WARNING}{self.__dataPath}{colors.FAIL} File do not exists{colors.ENDC}")
      return False
    return self.__checkDevice(deviceName)

  def __checkDevice(self, deviceName):
    i = 0
    for device in self.__data['devices']:
      name = deviceName
      if(len(deviceName)>=len(device['device'])):
        name = deviceName[0:len(device['device'])]
      if(device['device']==name):
        self.__targets +=1
        self.__deviceID =i
      i+=1
    if(-1 == self.__deviceID):
      print(f"{colors.WARNING}{self.__dataPath}{colors.FAIL} No instructions how to test {deviceName} device{colors.ENDC}")
      return False
    return True

  # def getModuleID(self,moduleName):
  #   id = 0
  #   for module in self.__data['devices'][self.__deviceID]['modules']:
  #     if(module['moduleName']==moduleName):
  #       return id
  #     id = id +1
  
  # def getModulesNames(self):
  #   modulesList = []
  #   for module in self.__data['devices'][self.__deviceID]['modules']:
  #     modulesList.append(module['moduleName'])
  #   return modulesList

  # def getModule(self,id):
  #   try:
  #     ret = self.__data['devices'][self.__deviceID]['modules'][id]
  #     return ret
  #   except:
  #     print(f"{colors.WARNING}{self.__dataPath}{colors.FAIL} file is empty or formatted incorrectly{colors.ENDC}")
  #     return False

  def getModules(self,modulesList):
    modules = []
    try:
      for module in self.__data['devices'][self.__deviceID]['modules']:
        for moduleName in modulesList:
          if (module['module']==moduleName):
            modules.append(module)
    except:
      print(f"{colors.WARNING}{self.__dataPath}{colors.FAIL} file is empty or formatted incorrectly{colors.ENDC}")
      return False
    return modules