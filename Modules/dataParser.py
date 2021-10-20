import json
import Modules.colors as colors

class Data:
  __data = None
  __dataPath  = 'data.json'
  def __init__(self):
      pass
  def openJson(self):
    try:
      self.file = open(self.__dataPath)
      self.__data = json.load(self.file)
      self.file.close()
      return True
    except:
      print(f"{colors.WARNING}{self.__dataPath}{colors.FAIL} file do not exists{colors.ENDC}")
      return False

  def checkModuleExists(self,moduleName):
    id = 0
    for module in self.__data['modules']:
      if(module['moduleName']==moduleName):
        return id
        break
      id = id +1
    print(f"{colors.WARNING}No instrucions how to test {colors.OKBLUE}{moduleName}{colors.WARNING} module{colors.ENDC}")
    return -1

  def getModule(self,id):
    try:
      ret = self.__data['modules'][id]
      return ret
    except:
      print(f"{colors.WARNING}{self.__dataPath}{colors.FAIL} file is empty or formatted incorrectly{colors.ENDC}")
      return False