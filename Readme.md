#### Router testing using python
##### Program supports only python3
##### Required pip packages for the program: 

  +  pyModbusTCP
  +  Paramiko

##### Arguments:

  +  -a/--address ->> Sets device address
  +  -p/--port    ->> Sets address port. By default is set to 22
  +  -u/--username ->> Sets ssh connection username. 
  +  -ps/--password ->> Sets ssh connection password.
  +  -mp/--modbus_port ->> Sets modbus port.

##### Mandatory arguments:

  +  Device address
  +  Modbus port
  +  Username
  +  Password

##### Program launch examples:

  + /bin/python3 ./main.py -a 192.168.1.1 -u root -ps Admin123 -mp 502
  + /bin/python3 ./main.py --address 192.168.1.2 -p 22 -u root -ps Admin123 --modbus_port 502