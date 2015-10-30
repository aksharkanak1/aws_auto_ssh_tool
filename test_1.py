#!/usr/bin/python

import Conf
import main
import sys


if __name__ == "__main__":
   config=Conf.conf("./conf.info")
   m=main.mainClass(config)
   m.makeConnectionToReg(config)
   m.updateRegionsList(config,"")
   print m.connToReg['us-west-2'].insts
   m.CreateActiveInstListOfAllRegions()
   print "The active list is %s" % str(m.runningInstList)

   
   m.updateRegionsOtherResource(config,"")
   m.dumpAwsResourceInfo()
   if config.checkIfMultiProcessingIsReq() == False:
       for i in m.connToReg['us-west-2'].insts[16] :
           i.actionWithInInst()
       m.dumpExceptionList("./abc")
       m.dumpResultSet()
   else :
       main.createWorkers(m)
       
