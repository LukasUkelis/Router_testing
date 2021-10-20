class Separate:
  __moduleData = None
  def __init__(self, moduleData):
    self.__moduleData = moduleData

  def getCommandsCount(self):
    return len(self.__moduleData['commands'])

  def getSshCommand(self,id):
    return self.__moduleData['commands'][id]['sshCommand']
  
  def getSection(self,id):
    return self.__moduleData['commands'][id]['commandValue']

  def getModbusCommand(self,id):
    return {'registerAddress':self.__moduleData['commands'][id]['registerAddress'],'numberOfReg':self.__moduleData['commands'][id]['numberOfReg'],'returnFormat':self.__moduleData['commands'][id]['returnFormat']}