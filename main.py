import Modules.testingModules as testingModules

def main():
  connectionInfo={'address':"192.168.1.1",'username':"root",'port':"22",'password':"Admin123",'modPort':"502"}
  test = testingModules.Testing()
  test.startTesting(connectionInfo)


if __name__ == "__main__":
    main()