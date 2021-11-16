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
    if(args['get'] == "serial"):
      return self.__ssh.executeCommand("mnf_info -s")

  def executeCommand(self,command):
    return self.__ssh.executeCommand(command)

  def GPS_info(self,args):
    return self.__ssh.executeCommand(f"ubus call gpsd position | jsonfilter -e '@.{args['get']}'")
  
  def mobile_Info(self,args):
    if(args['get'] == "signal"):
      return self.__ssh.executeCommand("gsmctl -q")
    if(args['get'] == "activeSim"):
      return self.__ssh.executeCommand("ubus call sim get | jsonfilter -e '@.sim'")
    if(args['get'] == "GSMoperator"):
      return self.__ssh.executeCommand("gsmctl -o")
    if(args['get'] == "temperature"):
      return self.__ssh.executeCommand("gsmctl -c")

  def getRamUsage(self):
    total = int(self.__ssh.executeCommand("ubus call system info | jsonfilter -e '@.memory.total'"))
    free = int(self.__ssh.executeCommand("ubus call system info | jsonfilter -e '@.memory.free'"))
    using = int(total - free)
    return round(using / total * 100,2)

  def getCpuUsage(self):
    return self.__ssh.executeCommand("cpu_usage_script.sh")

  def getModules(self):
    modules = ['system']
    lines = self.__ssh.getRawAnswer("uci show /etc/config/hwinfo")
    for line in lines:
      line = line.strip("\n")
      l = len(line)
      check = line[l-2:l-1]
      if(check == "1"):
        modules.append(line[14:l-4])
    return modules