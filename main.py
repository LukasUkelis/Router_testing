import Modules.testingModules as testingModules
import Modules.colors as colors
import signal
import argparse


__test = testingModules.Testing()

def stop(signal, frame):
    __test.stopTesting()

def main():
    connectionInfo=argumetsParser()
    if not connectionInfo:
        return False
    signal.signal(signal.SIGINT, stop)
    __test.startTesting(connectionInfo)

def argumetsParser():
    __address = ""
    __port  = 22 # by default
    __username = ""
    __password = ""
    __modPort = 502 # by default

    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--address', help='Device address.')
    parser.add_argument('-p','--port', help='Device port.')
    parser.add_argument('-u','--username', help='Username for ssh connection.')
    parser.add_argument('-ps','--password', help='Password for ssh connection.')
    parser.add_argument('-mp','--modbus_port', help='Modbus port.')
    
    args = parser.parse_args()
    if(args.address == None):
        print(f"{colors.FAIL}Enter device ip address !!!\r\n{colors.WARNING}Arguments format: -a/--address ip address{colors.ENDC}")
        return 0
    else:
        print(f"Device ip address: {colors.PUR}{args.address}{colors.ENDC}")

    __address = args.address

    if(args.port == None):
        print(f"Device port set to default: {colors.PUR}22{colors.ENDC}")
    else:
        print(f"Device port set to: {colors.PUR}{args.port}{colors.ENDC}")
        __port = args.port

    if(args.modbus_port == None):
        print(f"{colors.FAIL}Enter modbus port !!!\r\n{colors.WARNING}Arguments format: -mp/--modport port{colors.ENDC}")
        return 0
    else:
        print(f"Modbus port set to: {colors.PUR}{args.modbus_port}{colors.ENDC}")
        __modPort = args.modbus_port

    if(args.username ==None):
        print(f"{colors.FAIL}Enter username !!!\r\n{colors.WARNING}Arguments format: -u/--username username{colors.ENDC}")
        return False
    else:
        __username = args.username

    if(args.password ==None):
        print(f"{colors.FAIL}Enter password !!!\r\n{colors.WARNING}Arguments format: -ps/--password password{colors.ENDC}")
        return False
    else:
        __password = args.password
    return {'address':__address,'username':__username,'port':__port,'password':__password,'modPort':__modPort}



if __name__ == "__main__":
    main()