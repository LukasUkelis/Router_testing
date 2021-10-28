class Separate:
  
  __moduleData = None

  def __init__(self, moduleData):
    self.__moduleData = moduleData

  def getTargetsCount(self):
    return len(self.__moduleData['targets'])

  def getSshCommand(self,id):
    return self.__moduleData['targets'][id]['sshCommand']
  
  def getTarget(self,id):
    return self.__moduleData['targets'][id]['target']
  
  def getExtraComand(self,id):
    if(self.__moduleData['targets'][id]['extraComand'] == "null"):
      return False
    return self.__moduleData['targets'][id]['extraComand']

  def getModbusInstructions(self,id):
    return {'registerAddress':self.__moduleData['targets'][id]['registerAddress'],'numberOfReg':self.__moduleData['targets'][id]['numberOfReg'],'returnFormat':self.__moduleData['targets'][id]['returnFormat']}