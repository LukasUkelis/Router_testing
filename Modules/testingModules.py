import Modules.dataParser as dataParser 
import Modules.modbusConnection as modbusConnection
import Modules.writingToCSV as CSV
import Modules.colors as colors
import Modules.writingToConsole as consoleWriting
import Modules.sshCommandExecution as SSHCommands
import time

class Testing:
  
  # modules
  __data = None
  __ssh = None
  __modbus = None
  __csvWriter = None
  __console = None

  # variables
  __mobulesData = None
  __testingCout = 0
  __running = True
  __connectionInfo = None
  __higestRamUsage = 0
  __higestCpuUsage = 0
  __startTime = None
  __endOflast = 0
  __passed = 0
  __failed = 0
  

  def __init__(self):
    pass


  def __getModulesTestData(self,deviceName):
    self.__data = dataParser.Data()
    if not self.__data.openJson(deviceName):
      return False
    self.__mobulesData = self.__data.getModules(self.__getRouterModules())
    return True
    
    
  def __connectToSshAndModbus(self):
    self.__ssh = SSHCommands.execution(self.__connectionInfo)
    self.__modbus = modbusConnection.Connection(self.__connectionInfo)
    if not self.__ssh or not self.__modbus.connect():
      return False
    return True


  def __closeSshAndModbus(self):
    self.__modbus.closeConnection()
    self.__ssh.closeConnection()



  def __getModbusAnswer(self,command):
    answer = self.__modbus.readReg(command)
    self.__modbus.refresh()
    if not answer:
      return False
    return answer
  

  def __getRamUsage(self):
    total = int(self.__ssh.executeCommand("ubus call system info | jsonfilter -e '@.memory.total'"))
    free = int(self.__ssh.executeCommand("ubus call system info | jsonfilter -e '@.memory.free'"))
    using = int(total - free)
    return round(using / total * 100,2)

  def __getCPUUsage(self):
    return self.__ssh.executeCommand("cpu_usage_script.sh")


  def __ramUsageFormat(self, ramUsage):
    if(ramUsage > 65 and ramUsage <= 80):
      return f"{colors.WARNING}{ramUsage} %{colors.ENDC}"
    if(ramUsage > 80):
      return f"{colors.FAIL}{ramUsage} %{colors.ENDC}"
    return f"{colors.OKGREEN}{ramUsage} %{colors.ENDC}"

  def __cpuUsageFormat(self, cpuUsage):
    if(cpuUsage > 65 and cpuUsage <= 80):
      return f"{colors.WARNING}{cpuUsage} %{colors.ENDC}"
    if(cpuUsage > 80):
      return f"{colors.FAIL}{cpuUsage} %{colors.ENDC}"
    return f"{colors.OKGREEN}{cpuUsage} %{colors.ENDC}"


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
    modulesList = ['system']
    for module in self.__ssh.getModules():
      modulesList.append(module)
    return modulesList


  def __compareAnswers(self,sshAnswer,modbusAnswer,format):
    try:
      if not sshAnswer or not modbusAnswer:
        self.__failed +=1
        return "Error"
      if(format == "int" or format == "decimal"):
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
        sshAnswer = round(float(sshAnswer),lowerLen-1)
        modbusAnswer = round(float(modbusAnswer),lowerLen-1)
        if(sshAnswer==modbusAnswer):
          self.__passed+=1
          return "Passed"
      if(format == "string" or format == "IP"):
        if(sshAnswer==modbusAnswer):
          self.__passed+=1
          return "Passed"
      self.__failed +=1
      return "Failed"
    except:
      return "Error"


  def __testModule(self):

    self.__passed = 0
    self.__failed = 0
    
    for target in self.__mobulesData:
      sshAnswer =""
      if(self.__running == False):
        break
      modAnswer = self.__getModbusAnswer({'registerAddress':target['registerAddress'],'numberOfReg':target['numberOfReg'],'returnFormat':target['returnFormat']})
      try:
        method = getattr(self.__ssh,target['action'])
        sshAnswer = method(target['args'])
      except:
        self.__console.writeErrorInfo(f"{colors.WARNING}Action {colors.FAIL}{target['action']} {colors.WARNING}does not exist !!")

      status = self.__compareAnswers(sshAnswer,modAnswer,target['returnFormat'])
      self.__csvWriter.writeAnswer({'target':target['target'],'modbusAnswer':modAnswer,'sshAnswer':sshAnswer,'status':status})
      ramUsage = self.__getRamUsage()
      cpuUsage = self.__getCPUUsage()
      testInfo = {'cpu':self.__cpuUsageFormat(float(cpuUsage)),'currentTime':self.__timeFormat(time.time()-self.__startTime),'moduleName':target['module'],'target':target['target'],'modAnswer':modAnswer,'sshAnswer':sshAnswer,'passed':self.__passed,'failed':self.__failed,'ramUsage':self.__ramUsageFormat(ramUsage),'testCount':self.__testingCout}
      self.__console.writeTestInfo(testInfo)
      if(float(ramUsage)>float(self.__higestRamUsage)):
        self.__higestRamUsage = ramUsage
      if(float(cpuUsage)>float(self.__higestCpuUsage)):
        self.__higestCpuUsage = cpuUsage


  def startTesting(self,connectionInfo):
    self.__connectionInfo = connectionInfo
    if not self.__connectToSshAndModbus():
      return False
    deviceName = self.__ssh.executeCommand("uci get system.@system[0].routername")
    if not self.__getModulesTestData(deviceName):
      return False
    
    modulesList = self.__getRouterModules()
    if(len(modulesList)==0):
      print(f"{colors.FAIL}No modules to check{colors.ENDC}")
    else:
      self.__console  = consoleWriting.writing()
      self.__console.startWriting()
      deviceInfo = {'address':self.__connectionInfo['address'],'port':self.__connectionInfo['port'],'modPort':self.__connectionInfo['modPort'],'deviceName':deviceName}
      self.__csvWriter = CSV.formatData(deviceInfo)
      self.__csvWriter.openNewWriter()
      self.__csvWriter.writeTitle()
      self.__startTime = time.time()
      self.__endOflast = self.__startTime
      while True:
        passed = 0
        failed = 0
        self.__higestRamUsage = 0
        self.__higestCpuUsage = 0
        self.__testingCout += 1
        if(self.__running == True):
          self.__csvWriter.writeNewHeader(self.__testingCout)
        if(self.__running == False):
          self.__closeSshAndModbus()
          return True
        self.__testModule()
        passed += self.__passed
        failed += self.__failed
        self.__csvWriter.writeConclusions({'cpu':self.__higestCpuUsage,'duration':self.__timeFormat(time.time()-self.__endOflast),'passed':passed,'failed':failed,'ramUsage':self.__higestRamUsage})
        self.__endOflast = time.time()
      

  def stopTesting(self):
    self.__console.writeErrorInfo(f"{colors.FAIL}TEST STOPED{colors.ENDC}")
    self.__running = False
    