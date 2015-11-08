#!/usr/bin/python 
import imports
from boto.s3.connection import S3Connection
from boto.s3.key import Key

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

def uploadCallbackForS3(dataUploaded,totalSize):
    print "\n%d of %d uploaded\n" % (dataUploaded,totalSize)


def uploadFileToS3(bucket,fileName,conf):
    s3conn=S3Connection(conf.access_key_id, conf.access_key_sec)
    try:
           buck = s3conn.get_bucket(bucket)
    except :
           print "Failed to get the Bucket %s " % bucket
           return False
    try :
           keyFile=Key(buck,fileName)
           keyFile.set_contents_from_filename(fileName,replace=True,cb=uploadCallback,cbnum=10)
    except:
           print "Failed to Upload the file to S3"
           return False

    return True



                  
           
    
    
    
    
 
