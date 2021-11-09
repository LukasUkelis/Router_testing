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

##### Stoping program:
Press crtl + c to stop the program.

##### Configuration file:
###### Actions and arguments:
+ GPS_info
    + get 
        + latitude -> GPS latitude coordinate
        + longitude -> GPS longitude coordinate
        + accuracy -> GPS accuracy
        + speed -> GPS speed
        + satellites -> GPS satallite count
+ mobile_Info
    + get
        + signal -> Mobile signal strength (RSSI in dBm)
        + activeSim -> Active SIM card
+ device_info
    + get
        + mac -> LAN MAC address
        + name -> Router name
        + hostname -> Router hostname
        + uptime -> Router uptime
+ sentData
    + sim 
        + 1 -> get sent data from sim 1
        + 2 -> get sent data from sim 2
    + period
        + day -> mobile data sent per day
        + week -> mobile data sent per week
        + month -> mobile data sent per month
    + current
        + True -> enables current period (day = today).
        + False -> disenables current period (day = 24h).
+ receivedData
    + sim 
        + 1 -> get received data from sim 1
        + 2 -> get received data from sim 2
    + period
        + day -> mobile data received per day
        + week -> mobile data received per week
        + month -> mobile data received per month
    + current
        + True -> enables current period (day = today).
        + False -> disenables current period (day = 24h).
###### Configuration examples:

```
    {
              "target" : "Mobile data received last month (SIM2)",
              "returnFormat" : "int",
              "registerAddress" : "320",
              "numberOfReg" : "2",
              "module" : "dual_sim" ,
              "action" : "receivedData",
              "args" :
              {
                "sim":"2",
                "period":"month",
                "current":"False"
              }
    }
```
```
{
          "target" : "Mobile signal strength (RSSI in dBm)",
          "returnFormat" : "decimal",
          "registerAddress" : "3",
          "numberOfReg" : "2",
          "module" : "mobile" ,
          "action" : "mobile_Info",
          "args" : 
          {
            "get" : "signal"
          }
}
```
