#!/usr/bin/python

from pexpect import spawn,TIMEOUT,EOF 
import sys
import signal 
import os
import shutil
import random
import time
from multiprocessing import cpu_count
decryptFormat = "openssl aes-256-cbc -d -in %s -out %s "
tasksetFile = "/usr/bin/taskset"
taskSetCmdFmt = "/usr/bin/taskset -p 0x%x %d"
FROM_REMOTE_SYSTEM = 1 
INTO_REMOTE_SYSTEM = 2


def decryptFile(infile,outfile,password):
    cmd = decryptFormat % (infile,outfile)
    session = spawn(cmd)
    matched = session.expect(["password:",TIMEOUT,EOF],timeout = 1)
    if 0 == matched :
       session.sendline(password)
    elif 1 == matched or 2 == matched :
           return -1 
   
    matched = session.expect(EOF)
    return 0

def scpCopyfile(inst,ip,usr,fromloc,toloc,keyfile,tout,dir):
    if dir == FROM_REMOTE_SYSTEM:
        format ="scp -C -i %s %s@%s:%s %s"
        cmd = format % (keyfile,usr,ip,fromloc,toloc)
    else:
        format ="scp -C -i %s %s %s@%s:%s "
        cmd = format % (keyfile,fromloc,usr,ip,toloc)

    try :
        session = spawn(cmd)
        # I am expecting that the child process will not ask for any input
        matched = session.expect([TIMEOUT,EOF],timeout=tout)
        if 0 == matched :
           # the child process might be still be there so kill it 
           session.kill(signal.SIGTERM)
    except :
        inst.addToExcecptionList(sys.exc_info())
        raise

def getAwsCred(file):
    access_key_id = None
    access_key_sec = None
    try :
         fd = open(file,"r")
    except :
         return None,None

    for line in fd :
        line.strip()
        if line.startswith("ACCESS_KEY_ID="):
           access_key_id = line[len("ACCESS_KEY_ID="):].rstrip("\n")
             
        elif line.startswith("ACCESS_SECERT_KEY="):
           access_key_sec = line[len("ACCESS_SECERT_KEY="):].rstrip("\n")

    return access_key_id,access_key_sec

def copyAndZip(lst):
    dstFldr = "".join(["/tmp/",str(random.randint(1,20000000000)),"/"])
    if os.path.exists(dstFldr) != True:
       os.mkdir(dstFldr) 
    for i in lst:
        if i.endswith("/") == True:
           i=i.rstrip("/")
        finalPart=i[i.rfind("/")+1:]
        if os.path.isdir(i) == True :
           shutil.copytree(i,"".join([dstFldr,finalPart]))
        else: 
           shutil.copy(i,"".join([dstFldr,finalPart]))

    filePrefix = file="%d-%d-%d-%d-%d-%d" % (time.localtime().tm_year,time.localtime().tm_mon,time.localtime().tm_mday,time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec) 
    shutil.make_archive(filePrefix+"-result","gztar",root_dir=dstFldr,base_dir="./")
    finalFile="".join(["./",filePrefix,"-result",".tar.gz"])
    shutil.rmtree(dstFldr)
    if os.path.exists(finalFile):
       return finalFile
    
    return None 
    
def genForCpuAffinity(maxCpuToUse=0xffffffff):
    """
         API which can be used for generating the CPU affinity mask 
    """
    cpus=cpu_count()
    if maxCpuToUse == cpus or maxCpuToUse == 0xffffffff :
       maxCpuMask=0x1<<(cpus-1)
    else :
       maxCpuMask = 0x1 << (maxCpuToUse-1)
    cpumask=0x1
    while True :
          inp = yield
          if inp == "continue":
             yield cpumask
             cpumask = cpumask <<1
             if cpumask >  maxCpuMask:
                cpumask =0x1
          else :
             return 


def setCpuAffinityForProcess(pid,cpuMask):
    """
        API for setting the process cpu affinity   
    """
    if os.path.exists(tasksetFile) != True:
        return False 
    temp = 0x1<<(cpu_count()-1)
    if cpuMask > temp :
        return False 
    os.system(taskSetCmdFmt % (cpuMask))
    return True 


    
    
           
       
     
        
