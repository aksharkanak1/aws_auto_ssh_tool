#!/usr/bin/python 
import helper
import Instance
import sys
from prettytable import PrettyTable

StatusTblFormat = ["InstanceID","Status Code" ,"Status","Keyname","Pub Ip"]
IntfFormat = ["ENI-id","Private Addr ","Instance-id","status"]
kpformat = ["Name","Fingerprint"]
eipFromat = ["EIP","Instance-id","private address"]
sgTableFormat = ["name","rules"]

class regions():
      def __init__(self,conn,name,fil):
          self.conn = conn
          self.name = name
          self.fil = fil 
          self.insts ={}
          self.expList=[] 
          self.total = 0
          self.netIntf =[]
          self.eipList=[]
          self.keypair =[]          
          self.sgList = []
 
      def getList(self,conf):
          try :
              instList = helper.getInstList(self.conn)
          except :
              self.expList.append(sys.exc_info())
              return False 
          #convert the instance dictionary into intrenal format 
          for keys in instList.keys():
              for i,inst in enumerate(instList[keys]):
                  tempInst = Instance.InstanceClass(inst,conf) 
                  instList[keys][i] = tempInst
                  self.total +=1
          self.insts = instList
          return True 

      def getOtherResourceApartFromEC2Instances(self):
          #all excpetion will be ignored since other data is only for info sake 
          try :
               self.netIntf = self.conn.get_all_network_interfaces()
          except:
               pass
          try :
               self.eipList = self.conn.get_all_addresses()
          except:
               pass
          try :
               self.keypair = self.conn.get_all_key_pairs()
          except :
               pass      
          try :
               self.sgList = self.conn.get_all_security_groups()
               print self.sgList
          except:
               pass  

      def performActionWithInInstance(self,ran):
         """ This API will be used to perfrom action 
             with in Instances which belong to 
             specific region
         """
         [self.insts[16][i].actionWithInInst() for i in ran ]
         
      def dumpExpListForInst(self,fd):
          fd.write("Exception List for only active instances will be dumped \n") 
          if len(self.insts[16]) > 0:
             [self.insts[16][i].dumpException(fd) for i in range(len(self.insts[16]))]    
          else :
             fd.write("Zero Active instsance in the region")   

      def dumpExpListforRegion(self,fd,dumpForInsts=True):
          if len(self.expList) > 0:
             fd.write("Dumping the exception list for the region " +self.name+"\n")
             tbl = PrettyTable(["Sno","Exceptions"])
             for i,j in enumerate(self.expList) :
                 tbl.add_row([str(i),str(j)]) 
             fd.write(str(tbl))
             fd.write("\n") 
          if dumpForInsts:
             fd.write("Dumping the exception list also for the Insts in region"+self.name+"\n") 
             self.dumpExpListForInst(fd)   
          
      def fgetTotal(self):
          return self.total

      def dumpRegionResBasedOnInstState(self,key,fd):
          ran = len(self.insts[key])
          [self.insts[key][i].dumpResultOfInst(fd) for i in xrange(0,ran)] 

      def dumpRegionResult(self,fd):
          fd.write("Dumping the result for region " + self.name+"\n")
          #keys = self.insts.keys()
          #Currently only active instance will be considered 
          keys=[16]
          for i in keys :
              self.dumpRegionResBasedOnInstState(i,fd)

      def dumpSecurityGrpList(self,fd):
          sgTable = PrettyTable(sgTableFormat)
          for sgs in self.sgList:
              print sgs.name , sgs.rules
              sgTable.add_row([sgs.name,sgs.rules]) 
          #[sgTable.add_row([sgs.name,sgs.rules]) for sgs in self.sgList]
          fd.write(str(sgTable))
          fd.flush()        
 
      def dumpRegionInfo(self,fd):
          # dump the instance list 
          statusTbl = PrettyTable(StatusTblFormat)
          for key in self.insts.keys():
              if len(self.insts[key]) > 0 :
                 for inst in self.insts[key]:
                     instSt=inst.botoInstInfo._state
                     statusTbl.add_row([inst.botoInstInfo.id,instSt.code,instSt.name,inst.botoInstInfo.key_name,inst.botoInstInfo.ip_address])
          fd.write(str(statusTbl))
          fd.flush()
          #dump the network interface list
          if len(self.netIntf) > 0:
             IntfTable = PrettyTable(IntfFormat)
             for intf in self.netIntf:
                 eniid = intf.id
                 prip = intf.private_ip_address
                 attInst = intf.attachment
                 if intf.status == 'in-use' :
                    IntfTable.add_row([eniid,prip,attInst.instance_id,intf.status])
                 else:
                    IntfTable.add_row([eniid,prip,"NA",intf.status])
             fd.write(str(IntfTable))
             fd.flush()
          else :
             fd.write("\nNumber of network interface is 0\n")
          self.dumpSecurityGrpList(fd)  
          

      def getCachedInstList(self,key):
          return self.insts[key]         
