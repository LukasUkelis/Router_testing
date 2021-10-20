from os import truncate
from time import process_time_ns, sleep
import time
import dataParser 
import sshConection
import moduleDataSepar
import modbusConnection
import colors

class Testing:
  __data = None
  __ssh = None
  __modbus = None
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
    listToCheck = ["gps","mobile","dual_sim"]
    # listToCheck = ["gps"]
    modulesList = ['system']
    for element in listToCheck:
      answer = self.__getSSHAnswer(f"uci get hwinfo.@hwinfo[0].{element}")
      if(answer == "1"):
        modulesList.append(element)
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
    goback = "\033[F" * 9
    passed = 0
    failed = 0
    id = self.__data.checkModuleExists(moduleName)
    if (id == -1):
      return False
    data = self.__data.getModule(id)
    sep = moduleDataSepar.Separate(data)
    id = 0
    # print("-----------------------------------------------------------")
    # print(f"""
    #   {colors.OKBLUE}{moduleName}{colors.ENDC} module
    #   Testing {sep.getCommandsCount()} targets.

    #   Testing target:  
    #   Modbus answer:  
    #   SSH answer: 
    #   Passed:
    #   Failed:""")
    while id < sep.getCommandsCount():
      sshCommand = sep.getSshCommand(id)
      modbusCommand = sep.getModbusCommand(id)
      modAnswer = self.__getModbusAnswer(modbusCommand)
      sshAnswer = self.__getSSHAnswer(sshCommand)
      # print(self.__compareAnswers(sshAnswer,modAnswer,modbusCommand['returnFormat']))
      if not self.__compareAnswers(sshAnswer,modAnswer,modbusCommand['returnFormat']):
        failed = failed+1
      else:
        passed= passed +1
      print(f"""{goback}     
      {colors.OKBLUE}{moduleName}{colors.ENDC} module             
      Testing {colors.OKBLUE}{sep.getCommandsCount()}{colors.ENDC} targets.
                
      Testing target:  {colors.OKBLUE}{sep.getSection(id)}{colors.ENDC}                                  
      Modbus answer: {colors.OKBLUE}{modAnswer}{colors.ENDC}                               
      SSH answer: {colors.OKBLUE}{sshAnswer}{colors.ENDC}                             
      Passed: {colors.OKGREEN}{passed}{colors.ENDC}
      Failed: {colors.FAIL}{failed}{colors.ENDC}""")
      time.sleep(1)
      id = id +1
  def __writeToCSV(self,rowData):
    pass


  def testModules(self):
    connectionInfo={'address':"192.168.1.1",'username':"root",'port':"22",'password':"Admin123",'modPort':"502"}
    if not self.__getModulesTestData():
      return False
    if not self.__connectToSshAndModbus(connectionInfo):
      return False
    modulesList = self.__getRouterModules()
    if(len(modulesList)==0):
      print(f"{colors.FAIL}No modules to check{colors.ENDC}")
    else:
      print("\n"*9)
      for module in modulesList:
        self.__testModule(module)
    self.__closeSshAndModbus()

  
s = Testing()
s.testModules()