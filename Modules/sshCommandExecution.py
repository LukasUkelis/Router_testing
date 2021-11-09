import Modules.sshConection as sshConection

class execution:
  __ssh = None

  def __init__(self,connectionInfo):
    self.__ssh = sshConection.Connection(connectionInfo)
    self.__ssh.connect()
    if (self.__ssh ==False):
      return False

  def closeConnection(self):
    self.__ssh.closeConnection()
  
  def receivedData(self, args):
    a = "{"
    b = "}"
    return self.__ssh.executeCommand(f"ubus  call mdcollect get '{a}\"period\":\"{args['period']}\",\"sim\":{args['sim']},\"mode m\":\"3-1\",\"current\":{args['current']}{b}' | jsonfilter -e '@.rx'")
  
  def sentData(self, args):
    a = "{"
    b = "}"
    return self.__ssh.executeCommand(f"ubus  call mdcollect get '{a}\"period\":\"{args['period']}\",\"sim\":{args['sim']},\"mode m\":\"3-1\",\"current\":{args['current']}{b}' | jsonfilter -e '@.tx'")
  
  def device_Info(self,args):
    if(args['get'] == "mac"):
      return self.__ssh.executeCommand('mnf_info -m')
    if(args['get'] == "hostname"):
      return self.__ssh.executeCommand("ubus call system board | jsonfilter -e '@.hostname'")
    if(args['get'] == "name"):
      return self.__ssh.executeCommand("uci get system.@system[0].routername")
    if(args['get'] == "uptime"):
      return self.__ssh.executeCommand("ubus call system info | jsonfilter -e '@.uptime'")


  def executeCommand(self,command):
    return self.__ssh.executeCommand(command)
  
  def getModules(self):
    return self.__ssh.getModules()

  def GPS_info(self,args):
    return self.__ssh.executeCommand(f"ubus call gpsd position | jsonfilter -e '@.{args['get']}'")
  
  def mobile_Info(self,args):
    if(args['get'] == "signal"):
      return self.__ssh.executeCommand("gsmctl -q")
    if(args['get'] == "activeSim"):
      return self.__ssh.executeCommand("ubus call sim get | jsonfilter -e '@.sim'")