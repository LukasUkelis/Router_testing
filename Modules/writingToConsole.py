import Modules.colors as colors
import time

class writing:
  __goback = "\033[F" * 15
  
  def __init__(self):
    pass

  def __ramUsageFormat(self, ramUsage):
    if(float(ramUsage) > 65 and float(ramUsage) <= 80):
      return f"{colors.WARNING}{ramUsage} %{colors.ENDC}"
    if(float(ramUsage) > 80):
      return f"{colors.FAIL}{ramUsage} %{colors.ENDC}"
    return f"{colors.OKGREEN}{ramUsage} %{colors.ENDC}"

  def __cpuUsageFormat(self, cpuUsage):
    if(float(cpuUsage) > 65 and float(cpuUsage)<= 80):
      return f"{colors.WARNING}{cpuUsage} %{colors.ENDC}"
    if(float(cpuUsage) > 80):
      return f"{colors.FAIL}{cpuUsage} %{colors.ENDC}"
    return f"{colors.OKGREEN}{cpuUsage} %{colors.ENDC}"

  def startWriting(self):
    print(f"""       
                                                           
                                                          
                                                           
                                                           
                                                           
                                                           
                                                           
                                                          
                                                           
                                                           
                                                           
                                                          
                                                          
      """)
  
  def writeErrorInfo(self,errorInfo):
    self.__clearconsole()
    time.sleep(0.5)
    print(f"""{self.__goback}     
                                                           
                                                           
                                                           
                                                           
                                                           
                                                           
{errorInfo}{colors.ENDC}        
                                                           
                                                           
                                                  
                                                  
                                                              
                                                           
    """)
    time.sleep(2)
    self.__clearconsole()

  def writeConclusion(self,conclusionInfo):
    self.__clearconsole()
    print(f"""{self.__goback}
              {colors.OKCYAN}CONCLUSION{colors.ENDC}     
{colors.OKCYAN}-----------------------------------------------{colors.ENDC}
{colors.OKCYAN}Total test duration: {colors.PUR}{conclusionInfo['time']}{colors.ENDC}               
                                                           
{colors.OKCYAN}Total passed: {colors.OKGREEN}{conclusionInfo['passed']}{colors.ENDC}           
{colors.OKCYAN}Total failed: {colors.FAIL}{conclusionInfo['failed']}{colors.ENDC}                                                           

{colors.OKCYAN}Total test count: {colors.PUR}{conclusionInfo['testCount']}{colors.ENDC}

{colors.OKCYAN}Highest ram usage: {colors.PUR}{conclusionInfo['ram']} % {colors.OKCYAN}at {colors.PUR}{conclusionInfo['ramTestNum']}{colors.OKCYAN} test{colors.ENDC}                                                            
{colors.OKCYAN}Highest cpu usage: {colors.PUR}{conclusionInfo['cpu']} % {colors.OKCYAN}at {colors.PUR}{conclusionInfo['cpuTestNum']}{colors.OKCYAN} test{colors.ENDC}                                                             
{colors.OKCYAN}----------------------------------------------{colors.ENDC}      
              
    """)
  
  def __clearconsole(self):
    print(f"""{self.__goback}                                             
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                      
                                                                                                                    
                                                                                                                      
                                                                                                                       
                                                                                                                       
                                                                                                                       
      """)

  def writeTestInfo(self, testInfo):

    print(f"""{self.__goback}     
{colors.OKCYAN}----------------------------------------------{colors.ENDC}                 
Module -> {colors.OKBLUE}{testInfo['moduleName']}{colors.ENDC}             
Target -> {colors.OKBLUE}{testInfo['target']}{colors.ENDC}                                 
{colors.OKCYAN}----------------------------------------------{colors.ENDC}                               
Total passed: {colors.OKGREEN}{testInfo['totalPassed']}{colors.ENDC}                           
                                                                                
Total failed: {colors.FAIL}{testInfo['totalFailed']}{colors.ENDC}         
{colors.OKCYAN}----------------------------------------------{colors.ENDC}
Test duration: {colors.OKBLUE}{testInfo['currentTime']}{colors.ENDC} 
Test count: {colors.OKBLUE}{testInfo['testCount']}{colors.ENDC}  
Memory usage: {self.__ramUsageFormat(testInfo['ramUsage'])}       
CPU usage: {self.__cpuUsageFormat(testInfo['cpu'])}    
{colors.OKCYAN}----------------------------------------------{colors.ENDC}    
""")