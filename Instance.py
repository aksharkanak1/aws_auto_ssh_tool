#!/usr/bin/python 

import boto.ec2
from sshHelper import createSSHSession,executeCmdList,execCmd
from utils import scpCopyfile
from prettytable import PrettyTable
fileNameFormat = "%s"
import pdb
import random
import time
import sys
import utils
import Conf

class InstanceClass():
    def __init__(self,botoInstInfo,conf):
        self.botoInstInfo = botoInstInfo
        self.outFile = fileNameFormat % botoInstInfo.id
        self.ssh = None
        self.timeout = 25 
        self.expList =[]
        self.conf = conf
        self.cmdStatus= []
        self.scriptStatus=[] 

    def actionWithInInstRunCmds(self):
        #execute the comand list 
        fileName = str(random.randint(0x0,0xffffffff))+self.botoInstInfo.id
        self.fileName = fileName
        res=executeCmdList(self,fileName,self.conf.getCmdLists(),self.conf.debugon) 
        [self.cmdStatus.append(i) for i in res]

    def actionWithInInstRunScripts(self):
        for files in self.conf.scriptFiles:
           #copy the script files to the instance home directory 
           utils.scpCopyfile(self,self.botoInstInfo.ip_address,self.user,files,"/home/"+self.user,self.conf.getKeyFile(),self.timeout,utils.INTO_REMOTE_SYSTEM)
           # execute the script 
           res=execCmd(self,self.fileName,"./"+files,True)
	   self.scriptStatus.append(res)
        
    def actionWithInInstInit(self):
        if self.botoInstInfo.ip_address == None :
           return 
        for users in self.conf.getusers():
           try: 
               self.ssh = createSSHSession(self,self.botoInstInfo.ip_address,users,"",self.conf.getKeyFile()) 
               self.user=users
               break   
           except:
               print "Failed to create the ssh session" + str(sys.exc_info())
        
        return self.ssh 
         
    def actionWithInInst(self):
        self.actionWithInInstInit()
        if self.ssh == None:
           return 
        self.actionWithInInstRunCmds()
        self.actionWithInInstRunScripts()
        self.ssh.logout()
        self.getResultFile()          

    def getResultFile(self):
        #get the output file
        scpCopyfile(self,self.botoInstInfo.ip_address,self.user,"~/"+self.fileName,self.conf.res_folder+self.fileName,self.conf.getKeyFile(),self.timeout,utils.FROM_REMOTE_SYSTEM) 
        return 
   
    def actionOnInst(self):
        pass
   
    def addToExcecptionList(self,exp):
        self.expList.append(exp)

    def getExpList(self):
        return self.expList

    def dumpException(self,fd):
        if len(self.expList) > 0 :
           tbl = PrettyTable(["Sno","Exceptions"])
           tbl.max_width = 100
           for i,j in enumerate(self.expList) :
              tbl.add_row([str(i),str(j)])
           if self.conf.exp_op_type == Conf.SINGLE_FILE: 
              fd.write("Dumping the exception list for instance "+str(self.botoInstInfo)+"\n")
              fd.write(str(tbl))
              fd.write("\n")
              fd.flush()
           else :
              tempFlrStr = "".join([self.conf.exp_folder,self.botoInstInfo.id]) 
              tempfd = open(tempFlrStr,"w")
              tempfd.write(str(tbl))
              tempfd.write("\n")
              tempfd.flush()
              tempfd.close()  
        else:
           if self.conf.exp_op_type == Conf.SINGLE_FILE:
              fd.write("".join(["Exception list empty for  "],[str(self.botoInstInfo)],["\n"]))   
    
    def dumpResultOfInst(self,fd):
       tbl = PrettyTable(["Sno","cmd","result"])
       for i,j in enumerate(self.cmdStatus):
           tbl.add_row([str(i),self.conf.ListOfCmds[i],str(j)])
       if self.conf.res_op_type == Conf.SINGLE_FILE:
          fd.write("Dumping the cmd list result for instance "+str(self.botoInstInfo)+"\n")
          tempfd =fd
       else :
          tempfd = open("".join([self.conf.res_folder,self.botoInstInfo.id]),"w")
          tempfd.write(str(tbl))
          tempfd.write("\n")
       if len(self.conf.scriptFiles) > 0 :    
          tempfd.write("Dumping the script list result for instance "+str(self.botoInstInfo)+"\n")
          tbl = PrettyTable(["Sno","scripts","result"])
          for i,j in enumerate(self.scriptStatus):
              tbl.add_row([str(i),self.conf.scriptFiles[i],str(j)])    
          tempfd.write(str(tbl))
          tempfd.write("\n")
          tempfd.flush()
       else :
          tempfd.write("Zero script list for instance "+str(self.botoInstInfo)+"\n")
       if self.conf.res_op_type == Conf.MULTIPLE_FILES:
          tempfd.close()
 
