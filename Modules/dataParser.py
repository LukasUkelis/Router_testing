import json
import Modules.colors as colors
import Modules.dataParserHelper as helper

class Data:
  
  __data = None
  __dataPath  = 'data.json'
  __deviceID = -1

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
    i = helper.checkDevice(deviceName,self.__data['devices'])
    if(-1 == i):
      print(f"{colors.WARNING}{self.__dataPath}{colors.FAIL} No instructions how to test {deviceName} device{colors.ENDC}")
      return False
    self.__deviceID =i
    return True
    
  def getModules(self,modulesList):
    return helper.checkModules(modulesList,self.__data['devices'][self.__deviceID]['modules'])