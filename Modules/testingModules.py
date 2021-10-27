import Modules.dataParser as dataParser 
import Modules.sshConection as sshConection
import Modules.moduleDataSepar as moduleDataSepar
import Modules.modbusConnection as modbusConnection
import Modules.writingToCSV as CSV
import Modules.colors as colors
import Modules.writingToConsole as consoleWriting
import time

class Testing:
  # modules
  __data = None
  __ssh = None
  __modbus = None
  __csvWriter = None
  __console = None

  # variables
  __testingCout = 0
  __running = True
  __connectionInfo = None
  __higestRamUsage = 0
  __startTime = None
  __endOflast = 0
  __passed = 0
  __failed = 0
  

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
    return round(using / total * 100,2)

  def __ramUsageFormat(self, ramUsage):
    if(ramUsage > 65 and ramUsage <= 80):
      return f"{colors.WARNING}{ramUsage} %{colors.ENDC}"
    if(ramUsage > 80):
      return f"{colors.FAIL}{ramUsage} %{colors.ENDC}"
    return f"{colors.OKGREEN}{ramUsage} %{colors.ENDC}"

  def __timeFormat(self, Time):
    mi = Time/60
    mi = str(mi).split('.')[0]
    h = int(mi)/60  
    h = str(h).split('.')[0]
    mi = int(mi)%60
    sec = round(Time%60)
    if(int(h)>0 and int(mi)> 0):
      return f" {h}h. {mi}min. {sec}s."
    if(int(h) == 0 and int(mi)>0):
      return f" {mi}min. {sec}s."
    if(int(h)>0 and int(mi)== 0):
      return f" {h}h. {sec}s."
    return f" {sec}s."



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
      self.__failed +=1
      return "Error"
    if(format == "int"):
      try:
        sshAnswer = int(sshAnswer)
        modbusAnswer =int(modbusAnswer)
      except:
        sshAnswer = float(sshAnswer)
        modbusAnswer = float(modbusAnswer)
      if(sshAnswer==modbusAnswer):
        self.__passed+=1
        return "Passed"
    if(format == "float"):
      lowerLen  = min(len(str(sshAnswer).split('.')[1]),len(str(modbusAnswer).split('.')[1]))
      
      sshAnswer = round(float(sshAnswer),lowerLen)
      modbusAnswer = round(float(modbusAnswer),lowerLen)
      if(sshAnswer==modbusAnswer):
        self.__passed+=1
        return "Passed"
    if(format == "string" or format == "IP"):
      if(sshAnswer==modbusAnswer):
        self.__passed+=1
        return "Passed"
    self.__failed +=1
    return "Failed"

  def __testModule(self,moduleName):
    self.__passed = 0
    self.__failed = 0
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
      status = self.__compareAnswers(sshAnswer,modAnswer,modbusCommand['returnFormat'])
      self.__writeToCsv({'target':sep.getTarget(id),'modbusAnswer':modAnswer,'sshAnswer':sshAnswer,'status':status})
      ramUsage = self.__getRamUsage()
      testInfo = {'currentTime':self.__timeFormat(time.time()-self.__startTime),'moduleName':moduleName,'targetCout':sep.getTargetsCount(),'target':sep.getTarget(id),'modAnswer':modAnswer,'sshAnswer':sshAnswer,'passed':self.__passed,'failed':self.__failed,'ramUsage':self.__ramUsageFormat(ramUsage),'testCount':self.__testingCout}
      self.__console.writeTestInfo(testInfo)
      if(float(ramUsage)>float(self.__higestRamUsage)):
        self.__higestRamUsage = ramUsage
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
      self.__startTime = time.time()
      self.__endOflast = self.__startTime
      while True:
        passed = 0
        failed = 0
        self.__higestRamUsage = 0
        self.__testingCout += 1
        if(self.__running == True):
          self.__csvWriter.writeNewHeader(self.__testingCout)
        for module in modulesList:
          if(self.__running == False):
            self.__closeSshAndModbus()
            return True
          self.__testModule(module)
          passed += self.__passed
          failed += self.__failed
        self.__csvWriter.writeConclusions({'duration':self.__timeFormat(time.time()-self.__endOflast),'passed':passed,'failed':failed,'ramUsage':f"{self.__higestRamUsage} %"})
        self.__endOflast = time.time()
      

  def stopTesting(self):
    self.__console.writeErrorInfo(f"{colors.WARNING}After finishing testing current module program will exit{colors.ENDC}")
    self.__running = False
    


