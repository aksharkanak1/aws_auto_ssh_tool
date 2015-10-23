#!/usr/bin/python 

instKey = "instances"

class IntExcept:
      """ This Class holds infromation about the Exception that has occured"""
      def __init__(self,exceptInfo):
          pass
 
   
     

class IntExceptCollection:
      """ IntExceptCollection  will be used to hold the 
          Collection of all the exceptions that has occured
      """
      def __init__(self):
          instExpDict ={instKey:{}}  # Dict which will be contain the exceptions generated for instances 
          pass
     
      def updateInstExp(self,id,exp):
          try :
                 self.instExpDict[instKey][id]
          except :
                 self.instExpDict[instKey][id] =[]
          self.instExpDict[instKey][id].append(exp)

      def printExp(self):
          print 
      
