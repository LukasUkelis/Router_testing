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
    fileName = 'Testing_{time}.csv'.format(time=dt_string)
    self.__fileName = './Results/{filename}'.format(filename= fileName)
    self.__writer = open(self.__fileName,'w')
    return self.__fileName
  
  
  def closeWriter(self):
    self.__writer.close()
    time.sleep(1)

  def writeTitle(self):
      self.__writer.write("Address: {address}\r\n".format(address=self.__deviceInfo['address']))
      self.__writer.write("Port: {address}\r\n".format(address=self.__deviceInfo['port']))
      self.__writer.write("Modbus port: {address}\r\n\r\n".format(address=self.__deviceInfo['modPort']))
      rowWriter = csv.DictWriter(self.__writer,fieldnames=self.__fieldNames)
      rowWriter.writeheader()
      self.__writer.flush()

  def writeAnswer(self, answerData):
      rowWriter = csv.DictWriter(self.__writer,fieldnames=self.__fieldNames)
      rowWriter.writerow({'Target':answerData['target'],'Modbus answer':answerData['modbusAnswer'],'SSH answer':answerData['sshAnswer'],'Status':answerData['status']})
      self.__writer.flush()