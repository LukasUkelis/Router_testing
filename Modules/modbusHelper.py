import codecs
import struct
  
class helper:

  def __init__(self):
      pass
    
  def formatint(self,values):
    answer = ""
    for value in values:
      temp = bin(value)
      temp = temp[2:len(temp)]
      temp = ("0"*(16-len(temp)))+temp
      answer = answer + temp
    return f"{int(answer,2)}"

  def formatfloat(self,values):
    answer = ""
    answer = int(values[0])*65536+int(values[1])
    answer = hex(answer)
    answer = struct.unpack('!f', bytes.fromhex(answer[2:len(answer)]))[0]
    return f"{answer}"

  def formatdecimal(self,values):
    answer = ""
    value = values[1]
    temp = bin(~value & 0xFFFF )
    temp = temp[2:len(temp)]
    add = "1".zfill(16)
    temp = temp.zfill(16)
    carry =0
    for i in range(16 -1,-1,-1):
      r = carry
      r += 1 if temp[i] == '1' else 0
      r += 1 if add[i] == '1' else 0
      answer = ('1' if r % 2 == 1 else '0')+answer
      carry = 0 if r <2 else 1
    if carry !=0:
        answer = '1'+answer
    return f"-{int(answer,2)}"

  def formatstring(self,values):
    answer = ""
    for value in values:
      temp = hex(value)
      if(len(temp)>3):
        temp = temp[2:len(temp)]
        temp= codecs.decode(temp, "hex").decode('utf-8')
        answer = answer + temp
    return answer
    
  def formatIP(self,values):
    answer=" "
    i = 0
    for value in values:
      temp = bin(value)
      temp = temp[2:len(temp)]
      temp = ("0"*(16-len(temp)))+temp
      ip1 = int(temp[0:8],2)
      ip2 = int(temp[8:16],2)
      if(i==0):
        answer = f"{ip1}.{ip2}"
      else:
        answer = f"{answer}.{ip1}.{ip2}"
      i = 1
    return answer