import Modules.dataParser as dataParser 
import Modules.sshConection as sshConection
import Modules.moduleDataSepar as moduleDataSepar
import Modules.modbusConnection as modbusConnection
import Modules.writingToCSV as CSV
import Modules.colors as colors
import time

class Testing:
  __data = None
  __ssh = None
  __modbus = None
  __csvWriter = None
  def __init__(self):
      pass

  def __getModulesTestData(self):
    self.__data = dataParser.Data()
    if not self.__data.openJson():
      return False
    return True
    
    
  def __connectToSshAndModbus(self,connectionInfo):
    self.__ssh = sshConection.Connection(connectionInfo)
    self.__modbus = modbusConnection.Connection(connectionInfo)
    if not self.__ssh.connect() or not self.__modbus.connect():
      return False
    return True


  def __closeSshAndModbus(self):
    self.__ssh.closeConnection()


  def __getSSHAnswer(self,command):
    answer = self.__ssh.executeCommand(command)
    if not answer:
      return False
    return answer
  def __getModbusAnswer(self,command):
    answer = self.__modbus.readReg(command)
    self.__modbus.refresh()
    if not answer:
      return False
    return answer
  

  def __getRouterModules(self):
    listToCheck = self.__data.getModulesNames()
    modulesList = []
    for element in listToCheck:
      answer = self.__getSSHAnswer(f"uci get hwinfo.@hwinfo[0].{element}")
      if(answer == "1"):
        modulesList.append(element)
    print(f"Testing modules: {colors.OKBLUE}{modulesList}{colors.ENDC}")
    return modulesList

  def __compareAnswers(self,sshAnswer,modbusAnswer,format):
    if(format == "int"):
      try:
        if(int(sshAnswer)==int(modbusAnswer)):
          return True
      except:
        if(float(sshAnswer)==float(modbusAnswer)):
          return True
    if(format == "string"):
      if(sshAnswer==modbusAnswer):
        return True
    return False

  def __testModule(self,moduleName):
    goback = "\033[F" * 11
    passed = 0
    failed = 0
    id = self.__data.getModuleID(moduleName)
    if (id == -1):
      return False
    data = self.__data.getModule(id)
    sep = moduleDataSepar.Separate(data)
    id = 0
    while id < sep.getCommandsCount():
      sshCommand = sep.getSshCommand(id)
      modbusCommand = sep.getModbusCommand(id)
      modAnswer = self.__getModbusAnswer(modbusCommand)
      sshAnswer = self.__getSSHAnswer(sshCommand)
      status = "Error"
      if not self.__compareAnswers(sshAnswer,modAnswer,modbusCommand['returnFormat']):
        failed = failed+1
        status = "Failed"
      else:
        passed= passed +1
        status = "Passed"
      self.__writeToCsv({'target':sep.getSection(id),'modbusAnswer':modAnswer,'sshAnswer':sshAnswer,'status':status})

      print(f"""{goback}     
{colors.OKBLUE}{moduleName}{colors.ENDC} module             
Testing {colors.OKBLUE}{sep.getCommandsCount()}{colors.ENDC} targets.
                
Testing target:  {colors.OKBLUE}{sep.getSection(id)}{colors.ENDC}                                  
Modbus answer: {colors.OKBLUE}{modAnswer}{colors.ENDC}                               
SSH answer: {colors.OKBLUE}{sshAnswer}{colors.ENDC}                             
Passed: {colors.OKGREEN}{passed}{colors.ENDC}
Failed: {colors.FAIL}{failed}{colors.ENDC}

""")
      time.sleep(0.5)
      id = id +1

  def __writeToCsv(self,data):
    self.__csvWriter.writeAnswer(data)

  def startTesting(self,connectionInfo):
    if not self.__getModulesTestData():
      return False
    if not self.__connectToSshAndModbus(connectionInfo):
      return False
    modulesList = self.__getRouterModules()
    if(len(modulesList)==0):
      print(f"{colors.FAIL}No modules to check{colors.ENDC}")
    else:
      deviceName = self.__getSSHAnswer("uci get system.@system[0].routername")
      deviceInfo = {'address':connectionInfo['address'],'port':connectionInfo['port'],'modPort':connectionInfo['modPort'],'deviceName':deviceName,'modules':modulesList}
      self.__csvWriter = CSV.formatData(deviceInfo)
      self.__csvWriter.openNewWriter()
      self.__csvWriter.writeTitle()
      print("\n"*11)
      while True:
        try:
          for module in modulesList:
            self.__testModule(module)
        except KeyboardInterrupt:
          self.__closeSshAndModbus()
          print("Testing ended")
          return False
