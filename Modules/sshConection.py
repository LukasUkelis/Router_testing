import paramiko
import time
import Modules.writingToConsole as consoleWriting
import Modules.colors as colors
class Connection:
  __ssh = None
  __connectionInfo = None
  def __init__(self,connectionInfo):
    self.__connectionInfo = connectionInfo
    self.__console = consoleWriting.writing()

  def connect(self):
    host = self.__connectionInfo['address']
    port =self.__connectionInfo['port']
    username = self.__connectionInfo['username']
    password = self.__connectionInfo['password']
    self.__ssh = paramiko.SSHClient()
    self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      self.__ssh.connect(host,port=port,username=username,password=password)
    except:
      print(f"{colors.FAIL}SSH connection can not be established. Check: address, username, password and port{colors.ENDC}")
      time.sleep(1)
      return False
    return True

  def __parsingLines(self, lines):
    try:
      line = lines[0]
      line =line.strip("\n")
      return line
    except IndexError: 
      return False

    
    
  def executeCommand(self,command):
    try:
      stdin, stdout, stderr = self.__ssh.exec_command(command)
      time.sleep(0.5)
      lines = stdout.readlines()
    except:
      error  = f"{colors.WARNING}{command}{colors.FAIL} can`t be executed{colors.ENDC}"
      self.__console.writeErrorInfo(error)
      return False
    if not self.__parsingLines(lines):
      error  = f"{colors.WARNING}{command}{colors.FAIL} does`t return answer{colors.ENDC}"
      self.__console.writeErrorInfo(error)
      return False
    return self.__parsingLines(lines)
    
  def closeConnection(self):
    time.sleep(0.5)
    self.__ssh.close()
    time.sleep(0.5)
