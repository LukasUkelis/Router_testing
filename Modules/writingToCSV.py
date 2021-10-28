import csv
import time
from datetime import datetime

class formatData:
  __fileName = None
  __deviceInfo = None
  __writer = None

  __fieldNames = ['Target','Modbus answer','SSH answer','Status']

  def __init__(self,deviceInfo):
      self.__deviceInfo = deviceInfo

  def openNewWriter(self):
    now = datetime.now()
    dt_string = now.strftime('%d-%m-%Y_%H-%M-%S')
    fileName = '{deviceName}_testing_{time}.csv'.format(deviceName=self.__deviceInfo['deviceName'],time=dt_string)
    self.__fileName = './Results/{filename}'.format(filename= fileName)
    self.__writer = open(self.__fileName,'w')
    return self.__fileName
  
  
  def closeWriter(self):
    self.__writer.close()
    time.sleep(1)

  def writeNewHeader(self,testNumber):
      rowWriter = csv.DictWriter(self.__writer,fieldnames=self.__fieldNames)
      self.__writer.write(f"\r\nTest: {testNumber}\r\n")
      rowWriter.writeheader()
      self.__writer.flush()
    
  def writeConclusions(self, conclusionData):
      self.__writer.write(f"Test duration: {conclusionData['duration']}\r\n")
      self.__writer.write(f"Highest ram usage: {conclusionData['ramUsage']} %\r\n")
      self.__writer.write(f"Highest cpu usage: {conclusionData['cpu']} %\r\n")
      self.__writer.write(f"Passed: {conclusionData['passed']}\r\n")
      self.__writer.write(f"Failed: {conclusionData['failed']}\r\n")


  def writeTitle(self):
      self.__writer.write("Device name: {deviceName}\r\n".format(deviceName=self.__deviceInfo['deviceName']))
      self.__writer.write("Address: {address}\r\n".format(address=self.__deviceInfo['address']))
      self.__writer.write("Port: {address}\r\n".format(address=self.__deviceInfo['port']))
      self.__writer.write("Modbus port: {address}\r\n\r\n".format(address=self.__deviceInfo['modPort']))
      self.__writer.write("Testing modules: {address}\r\n\r\n".format(address=self.__deviceInfo['modules']))
      self.__writer.flush()

  def writeAnswer(self, answerData):
      rowWriter = csv.DictWriter(self.__writer,fieldnames=self.__fieldNames)
      rowWriter.writerow({'Target':answerData['target'],'Modbus answer':answerData['modbusAnswer'],'SSH answer':answerData['sshAnswer'],'Status':answerData['status']})
      self.__writer.flush()