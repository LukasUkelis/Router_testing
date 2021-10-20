import Modules.testingModules as testingModules

def main():
  connectionInfo={'address':"192.168.1.1",'username':"root",'port':"22",'password':"Admin123",'modPort':"502"}
  test = testingModules.Testing()
  test.startTesting(connectionInfo)
  # csvWriter = CSV.formatData(connectionInfo)
  # filePath = csvWriter.openWriter()
  # csvWriter.writeTitle()
  # test = testingModules.Testing()
  # print("\n"*9)
  # while True:
  #   try:
  #     test.startTesting(connectionInfo,filePath)
  #     csvWriter.writeAnswer({'target':"something",'modbusAnswer':"modbus",'sshAnswer':"ssh",'status':"passed"})
  #     time.sleep(0.5)
  #   except KeyboardInterrupt:
  #     test.stopTesting()
  #     print("testavimas baigtas")
  #     sys.exit()


if __name__ == "__main__":
    main()