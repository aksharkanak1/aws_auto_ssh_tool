#!/usr/bin/python 
import imports

ALL=100
PENDING=0
RUNNING=16
SHUTTING_DONW=32
TERMINATED=48
STOPPING = 64
STOPPED=80

#function to get the list instance to work upon
def getInstList(conn):
    """ This function will be returning the instances
        The return is dictionary 
    """ 
    output ={PENDING:[],RUNNING:[],SHUTTING_DONW:[],TERMINATED:[],STOPPING:[],STOPPED:[]}

    #get the list off all the instance 
    Instlist = conn.get_only_instances()
    if len(Instlist) > 0:
       for inst in Instlist :
           instSt=inst._state
           if instSt.code in output.keys():
              output[instSt.code].append(inst)

    return output




                  
           
    
    
    
    
 
