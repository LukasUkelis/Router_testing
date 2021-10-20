from pyModbusTCP.client import ModbusClient
import Modules.colors as colors
import time
import codecs

class Connection:
  __connectionInfo = None
  __client = None
  def __init__(self,connectionInfo):
    self.__connectionInfo = connectionInfo
    
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
    time.sleep(0.4)
    self.__client.open()


  def __formatInt(self,values):
    answer = ""
    for value in values:
      temp = bin(value)
      temp = temp[2:len(temp)]
      temp = ("0"*(16-len(temp)))+temp
      answer = answer + temp
    return f"{int(answer,2)}"

  def __formatFloat(self,values):
    answer = ""
    for value in values:
      temp = bin(value)
      temp = temp[2:len(temp)]
      temp = ("0"*(16-len(temp)))+temp
      answer = answer + temp
    return f"{int(answer)}"


  def __formatHexString(self,values):
    answer = ""
    for value in values:
      temp = hex(value)
      if(len(temp)>3):
        temp = temp[2:len(temp)]
        temp= codecs.decode(temp, "hex").decode('utf-8')
        answer = answer + temp
    return answer
    
  def __formatIP(self,values):
    answer=""
    for value in values:
      temp = bin(value)
      temp = temp[2:len(temp)]
      temp = ("0"*(16-len(temp)))+temp
      ip1 = int(temp[0:8],2)
      ip2 = int(temp[8:16],2)
      if(i==0):
        answer = f"{ip1}.{ip2}"
      else:
        answer = f"{answer}.{ip1}.{ip2}"
      i = 1
    return answer

  def readReg(self,readInfo):
    try:
      values = self.__client.read_holding_registers(int(readInfo['registerAddress']),int(readInfo['numberOfReg']))
    except:
      print(f"{colors.FAIL}Can't get information from {colors.OKBLUE}{readInfo['registerAddress']}{colors.FAIL} register{colors.ENDC}")
      return False

    if (values != None):
      if(readInfo['returnFormat']=="string"):
        return self.__formatHexString(values)
      if(readInfo['returnFormat']=="int"):
        return self.__formatInt(values)
      if(readInfo['returnFormat']=="ip"):
        return self.__formatIP(values) 
      if(readInfo['returnFormat']=="float"):
        return self.__formatFloat(values)
    print(f"{colors.FAIL}Can't get information from {colors.OKBLUE}{readInfo['registerAddress']}{colors.FAIL} register{colors.ENDC}")
    return False