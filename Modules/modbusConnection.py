from pyModbusTCP.client import ModbusClient
import Modules.writingToConsole as consoleWriting
import Modules.colors as colors
import Modules.modbusHelper as modbusHelper
import time

class Connection:
  __connectionInfo = None
  __client = None
  __console = None
  __helper = None

  def __init__(self,connectionInfo):
    self.__connectionInfo = connectionInfo
    self.__console = consoleWriting.writing()
    self.__helper = modbusHelper.helper()
    
  def connect(self):
    try:
      self.__client = ModbusClient(host=self.__connectionInfo['address'],port=self.__connectionInfo['modPort'])
      self.__client.open()
    except:
      print(f"{colors.FAIL}Modbus connection can not be established. Check: address and port, ensure that router supports modbus{colors.ENDC}")
      return False
    if not self.__client.is_open():
      print(f"{colors.FAIL}Modbus connection can not be established. Check: address and port, ensure that router supports modbus{colors.ENDC}")
      return False
    return True

  def refresh(self):
    self.__client.close()
    self.__client.open()

  def closeConnection(self):
    self.__client.close()

  def __dynamicFormatCall(self,formatType,values):
    methodName = f"format{formatType}"
    try:
      method = getattr(self.__helper,methodName)
    except:
      error  = f"{colors.FAIL}No instructions for how to format {colors.WARNING}{formatType}{colors.ENDC}"
      self.__console.writeErrorInfo(error)
      return "  "
    return method(values)

  def readReg(self,readInfo):
    try:
      values = self.__client.read_holding_registers(int(readInfo['registerAddress']),int(readInfo['numberOfReg']))
    except:
      if self.__client.is_open():
        error  = f"{colors.FAIL}Can't get information from {colors.OKBLUE}{readInfo['registerAddress']}{colors.FAIL} register{colors.ENDC}"
        self.__console.writeErrorInfo(error)
        return False
      self.__checkConnection()
      return self.readReg(readInfo)
    if (values != None):
      return self.__dynamicFormatCall(readInfo['returnFormat'],values)
    self.refresh()
    if self.__client.is_open():
      error  = f"{colors.FAIL}Can't get information from {colors.OKBLUE}{readInfo['registerAddress']}{colors.FAIL} register{colors.ENDC}"
      self.__console.writeErrorInfo(error)
      return False
    self.__checkConnection()
    return self.readReg(readInfo)

  def __checkConnection(self):
    while True:
      error  = f"           {colors.FAIL}Modbus connection lost{colors.ENDC}"
      self.__console.writeErrorInfo(error)
      if self.__client.is_open():
        error  = f"           {colors.OKGREEN}Modbus connection restored{colors.ENDC}"
        self.__console.writeErrorInfo(error)
        break
      time.sleep(0.3)
      self.refresh()
    return True
    