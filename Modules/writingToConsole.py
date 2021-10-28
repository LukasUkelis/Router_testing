import Modules.colors as colors
import time

class writing:
  __goback = "\033[F" * 16
  
  def __init__(self):
    pass

  def startWriting(self):
    print(f"""       
                                                           
                                                          
                                                           
                                                           
                                                           
                                                           
                                                           
                                                          
                                                           
                                                           
                                                           
                                                           
                                                          
                                                          
      """)
  
  def writeErrorInfo(self,errorInfo):
    self.__clearconsole()
    time.sleep(0.5)
    print(f"""{self.__goback}     
                                                           
                                                           
                                                           
                                                           
                                                           
{colors.FAIL}{errorInfo}{colors.ENDC}        
                                                           
                                                           
                                                  
                                                  
                                                         

                                                              
                                                           
    """)
    time.sleep(2)
    self.__clearconsole()
  
  def __clearconsole(self):
    print(f"""{self.__goback}                                             
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                    
                                                                                                                      
                                                                                                                      
                                                                                                                       
                                                                                                                       
                                                                                                                       
      """)

  def writeTestInfo(self, testInfo):

    print(f"""{self.__goback}     
{colors.OKBLUE}{testInfo['moduleName']}{colors.ENDC} module             
Testing {colors.OKBLUE}{testInfo['targetCout']}{colors.ENDC} targets.
                
Testing target:  {colors.OKBLUE}{testInfo['target']}{colors.ENDC}                                  
Modbus answer: {colors.OKBLUE}{testInfo['modAnswer']}{colors.ENDC}                               
SSH answer: {colors.OKBLUE}{testInfo['sshAnswer']}{colors.ENDC}                                     
Passed: {colors.OKGREEN}{testInfo['passed']}{colors.ENDC}     
Failed: {colors.FAIL}{testInfo['failed']}{colors.ENDC}    


Test duration: {colors.OKBLUE}{testInfo['currentTime']}{colors.ENDC} 
Test count: {colors.OKBLUE}{testInfo['testCount']}{colors.ENDC}  
Memory usage: {testInfo['ramUsage']}  
CPU usage: {testInfo['cpu']} 
""")