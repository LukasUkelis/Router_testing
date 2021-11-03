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
  
  def simGet(self,args):
    return self.__ssh.executeCommand("ubus call sim get | jsonfilter -e '@.sim'")
  
  def mnfinfo(self,args):
    return self.__ssh.executeCommand('ubus call mnfinfo get | jsonfilter -e \'@.mnfinfo.{s}\''.format(s = args))

  def executeCommand(self,command):
    return self.__ssh.executeCommand(command)
  
  def getModules(self):
    return self.__ssh.getModules()

  def position(self,args):
    return self.__ssh.executeCommand(f"ubus call gpsd position | jsonfilter -e '@.{args}'")
  
  def signal(self,args):
    return self.__ssh.executeCommand("gsmctl -q")