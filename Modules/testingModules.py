import Modules.dataParser as dataParser 
import Modules.sshConection as sshConection
import Modules.moduleDataSepar as moduleDataSepar
import Modules.modbusConnection as modbusConnection
import Modules.writingToCSV as CSV
import Modules.colors as colors
import Modules.writingToConsole as consoleWriting

class Testing:
  __data = None
  __ssh = None
  __modbus = None
  __csvWriter = None
  __console = None
  __testingCout = 0
  __running = True
  __connectionInfo = None
  

  def __init__(self):
    pass

  def __getModulesTestData(self):
    self.__data = dataParser.Data()
    if not self.__data.openJson():
      return False
    return True
    
    
  def __connectToSshAndModbus(self):
    self.__ssh = sshConection.Connection(self.__connectionInfo)
    self.__modbus = modbusConnection.Connection(self.__connectionInfo)
    if not self.__ssh.connect() or not self.__modbus.connect():
      return False
    return True


  def __closeSshAndModbus(self):
    self.__modbus.closeConnection()
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
  
  def __getRamUsage(self):
    total = int(self.__getSSHAnswer("ubus call system info | jsonfilter -e '@.memory.total'"))
    free = int(self.__getSSHAnswer("ubus call system info | jsonfilter -e '@.memory.free'"))
    using = int(total - free)
    usage =round(using / total * 100,2)
    if(usage > 65 and usage <= 80):
      return f"{colors.WARNING}{usage} %{colors.ENDC}"
    if(usage > 80):
      return f"{colors.FAIL}{usage} %{colors.ENDC}"
    return f"{colors.OKGREEN}{usage} %{colors.ENDC}"
  



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
    if not sshAnswer or not modbusAnswer:
      return "Error"
    if(format == "int"):
      try:
        if(int(sshAnswer)==int(modbusAnswer)):
          return True
      except:
        if(float(sshAnswer)==float(modbusAnswer)):
          return True
    if(format == "float"):
      lowerLen  = min(len(str(sshAnswer).split('.')[1]),len(str(modbusAnswer).split('.')[1]))
      sshAnswer = round(float(sshAnswer),lowerLen)
      modbusAnswer = round(float(modbusAnswer),lowerLen)
      if(sshAnswer==modbusAnswer):
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
    while id < sep.getTargetsCount():
      sshCommand = sep.getSshCommand(id)
      modbusCommand = sep.getModbusInstructions(id)
      modAnswer = self.__getModbusAnswer(modbusCommand)
      sshAnswer = self.__getSSHAnswer(sshCommand)
      status = "Error"
      compared = self.__compareAnswers(sshAnswer,modAnswer,modbusCommand['returnFormat'])
      if (compared!="Error"):
        if not compared:
          failed +=1
          status = "Failed"
        else:
          passed +=1
          status = "Passed"
      self.__writeToCsv({'target':sep.getTarget(id),'modbusAnswer':modAnswer,'sshAnswer':sshAnswer,'status':status})
      ramUsage = self.__getRamUsage()
      testInfo = {'moduleName':moduleName,'targetCout':sep.getTargetsCount(),'target':sep.getTarget(id),'modAnswer':modAnswer,'sshAnswer':sshAnswer,'passed':passed,'failed':failed,'ramUsage':ramUsage,'testCount':self.__testingCout}
      self.__console.writeTestInfo(testInfo)
      id += 1

  def __writeToCsv(self,data):
    self.__csvWriter.writeAnswer(data)

  def startTesting(self,connectionInfo):
    self.__connectionInfo = connectionInfo
    if not self.__getModulesTestData():
      return False
    if not self.__connectToSshAndModbus():
      return False
    modulesList = self.__getRouterModules()
    if(len(modulesList)==0):
      print(f"{colors.FAIL}No modules to check{colors.ENDC}")
    else:
      self.__console  = consoleWriting.writing()
      self.__console.startWriting()
      deviceName = self.__getSSHAnswer("uci get system.@system[0].routername")
      deviceInfo = {'address':self.__connectionInfo['address'],'port':self.__connectionInfo['port'],'modPort':self.__connectionInfo['modPort'],'deviceName':deviceName,'modules':modulesList}
      self.__csvWriter = CSV.formatData(deviceInfo)
      self.__csvWriter.openNewWriter()
      self.__csvWriter.writeTitle()
      while True:
        self.__testingCout += 1
        for module in modulesList:
          if(self.__running == False):
            self.__closeSshAndModbus()
            return True
          self.__testModule(module)
      

  def stopTesting(self):
    self.__console.writeErrorInfo(f"{colors.WARNING}After finishing testing current module program will exit{colors.ENDC}")
    self.__running = False
    


