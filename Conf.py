#!/usr/bin/python

from utils import getAwsCred

FROM_OUTSIDE = 1
FROM_INSIDE = 2

SINGLE_FILE = 1
MULTIPLE_FILES = 2

class conf:

     def parseConfFile(self,file):
         try :
             fd = open(file,"r")
         except :  #TBD put code for IOError and write our own generic excpetion
             raise 
         for line in fd :
             line = line.strip()  #clear the starting white space 
             if line.startswith("cred_file "):
                temp = line[len("cred_file "):]
                self.cred_file = temp
 
             if line.startswith("keys "):
                temp = line[len("keys "):]
                self.keyfile = temp.split(",") 
              
             if line.startswith("users "):
                temp=line[len("users "):]
                self.users = temp.split(",")
 
             if line.startswith("regions "):
                temp=line[len("regions "):]
                self.regions = temp.split(",")
 
             if line.startswith("cmds "):
                temp=line[len("cmds "):]
                self.cmdsFiles = temp.split(",") 
                print self.cmdsFiles
                for files in  self.cmdsFiles:
                    with open(files,'r') as fd : 
                         for templine in fd :
                             templine = (templine.rstrip("\n")).strip()
                             if len(templine) >0 : 
                                self.ListOfCmds.append(templine)
   
             if line.startswith("debugon"):
                self.debugon = True
              
             if line.startswith("scripts "):
                temp=line[len("scripts "):] 
                self.scriptFiles = temp.split(",")   
    
             if line.startswith("mode"):
                temp=line[len("mode "):]
                if temp == 'outside': 
                   self.mode = FROM_OUTSIDE
                else :
                   self.mode = FROM_INSIDE   
  
             if line.startswith("resultfile "):
                temp=line[len("resultfile "):]
                self.resultFile = temp

             if line.startswith("exception_op_type"):
                temp=line[len("exception_op_type "):]
                if temp == 'multiple': 
                   self.exp_op_type = MULTIPLE_FILES

             if line.startswith("result_op_type"):
                temp=line[len("result_op_type "):]
                if temp == 'multiple': 
                   self.res_op_type = MULTIPLE_FILES

             if line.startswith("exception_folder"):
                self.exp_folder=line[len("exception_folder "):]

             if line.startswith("result_folder"):
                self.res_folder=line[len("result_folder "):]

             if line.startswith("aws_res_info"):
                temp=line[len("aws_res_info "):]
                self.awsInfoFile = temp
         
             if line.startswith("process "):
                temp=line[len("process "):]
                self.num_process = int(temp)

             if line.startswith("S3Bucket"):
                self.S3Loc=line[len("S3Bucket "):]
         return 

     def __init__(self,confFile):
         self.users=[]
         self.keyfile =[]
         self.regions=[]
         self.cmdsFiles=[]
         self.ListOfCmds=[]
         self.scripts =[] 
         self.exp_op_type = SINGLE_FILE
         self.res_op_file = SINGLE_FILE
         self.cred_file = None
         self.num_process =0
         self.scriptFiles=[]
         self.S3Loc=None
         self.parseConfFile(confFile)
         self.access_key_id = None
         self.access_key_sec =  None 
         self.access_key_id,self.access_key_sec = getAwsCred(self.cred_file)
         if self.access_key_id == None or self.access_key_sec == None:
            print "THE CREDS ARE NOT VALID"
            quit()  
         self.opFldrFileList=[]
         self.opFldrFileList.append(self.awsInfoFile)
         self.opFldrFileList.append(self.res_folder)
         self.opFldrFileList.append(self.exp_folder)
             
 
     def printOnScreen(self):
         print "users ", self.users
         print "keyfiles ", self.keyfile
         print "regions ", self.regions
         print "cmds ", self.ListOfCmds
         print "debug on ", str(self.debugon)
         print "scripts " , self.scriptFiles
    
     def getCmdLists(self):
         return self.ListOfCmds        
    
     def getKeyFile(self):
         return self.keyfile[0] # only one key files i supported as of now    

     def getRegionList(self):
         return self.regions
  
     def getusers(self):
         return self.users

     def getNumOfProcess(self):
         return self.num_process

     def getopFldrFileList(self):
         return self.opFldrFileList

     def getS3Loc(self):
         return self.S3Loc  
   
     def checkIfMultiProcessingIsReq(self):
         if self.num_process == None or self.num_process == 0:
            return False
         return True     
