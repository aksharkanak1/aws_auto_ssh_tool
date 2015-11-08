#!/usr/bin/python

import boto.ec2
import regions
import Conf
import multiprocessing
class mainClass:
      def __init__(self,conf):
          self.regions=conf.getRegionList()
          self.connToReg={}
          self.Quota = {}
          self.conf =conf
          self.runningInstList=[]

      def makeConnectionToReg(self,conf):
          for reg in self.regions:
              conn = boto.ec2.connect_to_region(reg,aws_access_key_id=conf.access_key_id,aws_secret_access_key=conf.access_key_sec,debug=10)
              self.connToReg[reg]=regions.regions(conn,reg,"",conf)    

      def updateRegionsList(self,conn,fil):
          for reg in  self.connToReg.keys():
              self.connToReg[reg].getList(self.conf)

      def updateRegionsOtherResource(self,con,fil):
          for reg in  self.connToReg.keys():
              self.connToReg[reg].getOtherResourceApartFromEC2Instances()
 
      def updateRunningInstList(self):
          for reg in self.connToReg.keys():
              [self.runningInstList.append(inst) for inst in self.connToReg[reg][16]]

      def performActionWithInst(self,ran):
          """ This API will be performing action with in 
              The instances 
          """ 
          for reg in  self.connToReg.keys():
              regdata = self.connToReg[reg]
              regdata.performActionWithInInstance(ran)


      def dumpExceptionList(self,fileName,dumpForInsts=True):
          fd =  open(fileName,"w")
          regList = self.connToReg.keys()
          [self.connToReg[reg].dumpExpListforRegion(fd,dumpForInsts) for reg in regList]
          fd.flush() 
          fd.close()
           
      def perfromActionWithInstWhichBecameActive(self):
          """
              It might be possible that some of the instance were just 
              booting up when the query was made .  
          """           
          pass 

      def dumpResultSet(self):
          """
               Dumps the result from all the instance into a file 
          """ 
           
          fd = open(self.conf.resultFile,"w")
          keys = self.connToReg.keys()   
          [self.connToReg[key].dumpRegionResult(fd) for key in keys]
 
      def dumpAwsResourceInfo(self):
          fd = open(self.conf.awsInfoFile,"w")
          keys = self.connToReg.keys()   
          [self.connToReg[key].dumpRegionInfo(fd) for key in keys]

      def CreateActiveInstListOfAllRegions(self):
          for reg in  self.connToReg.keys():
              self.runningInstList +=self.connToReg[reg].getCachedInstList(16)
    

      def execTaskOnEachRunningInst(self,instIndx):
          self.runningInstList[instIndx].actionWithInInst()      
          self.runningInstList[instIndx].dumpException(None)
          self.runningInstList[instIndx].dumpResultOfInst(None)

      def execTaskForInstsList(self,fromIdx,toIdx):
          [self.execTaskOnEachRunningInst(i) for i in range(fromIdx,toIdx+1)]

      def getRunningInstList(self):
          return self.runningInstList

      def uploadFinalResultToS3(self):
          if self.conf.getS3Loc() == None:
             finalFile=utils.copyAndZip(self.conf.getopFldrFileList())
             helper.uploadFileToS3(self.getS3Loc(),finalFile,self.conf)

def workerProcess(m,fromIdx,toIdx):
    m.execTaskForInstsList(fromIdx,toIdx) 

def createWorkers(m) :
    num_process = m.conf.getNumOfProcess()
    runInstLen = len(m.getRunningInstList())
    m.list_process=[]
    instStart=0
    delta=0
    if runInstLen <= num_process:
       instEnd = 0
       interval= 0
       num_process = runInstLen 
    else :
       interval = runInstLen/num_process
       delta = runInstLen%num_process
       instEnd=interval-1
    for i in range (0,num_process):
        m.list_process.append(multiprocessing.Process(target=workerProcess,args=(m,instStart,instEnd)))
        m.list_process[i].start()
        print "Started Process "+str(m.list_process[i])+" start  "+str(instStart)+" end "+str(instEnd)
        instStart=instEnd+1
        if interval ==0 :
           instEnd = instStart
        else :
           if (instEnd+interval) > runInstLen:
              instEnd = runInstLen-1
           else:
              if i == num_process-2 : # if last process then add delta also 
                 instEnd+=interval+delta
              else: 
                 instEnd+=interval

    # wait until all the child process dead 
    for p in m.list_process:
        p.join()
    
               
