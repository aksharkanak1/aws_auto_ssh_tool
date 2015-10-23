#!/usr/bin/python 
import paramiko
import socket
import copy 
import pxssh
import sys

cmdBannerFromat1 = "\""+"#"*40+"START"+"#"*40+"\""
cmdBannerFormat2 = "Cmd : %s"
cmdBannerFormat3 = "\""+"#"*40+"END"+"#"*40+"\""

def generateSSHShell(ip,**kwargs):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try :
        user=kwargs['username']
    except :
        print "username name not provided "
        return None
   
    try :
        passwd=kwargs['password']
    except :
        passwd = ""
    
    try :
        keyFile= kwargs['key_filename']          
    except :
        keyFile = ""

    try :
       ssh.connect(ip,username=user,password=passwd,key_filename=keyFile)
       shell = ssh.invoke_shell()
    except :
       print "Failed while creating shell "
       shell = None 
    
    return ssh,shell

def getStatusOfCmdExec(inst):
    try :
         inst.ssh.sendline("echo $?")
         inst.ssh.prompt()
         print inst.ssh.before
    except :
         #incase if there is failure in ssh then will return 0xffffffff    
         inst.addToExcecptionList(sys.exc_info())
         return 0xffffffff
    stStr=inst.ssh.before # will be in the fromat 'echo $?\r\n0\r\n'

    if not stStr.startswith("echo $?\r\n"):
         return 0xfffffffe
    else :
         try :
             stStr = stStr[len("echo $?\r\n"):]  
             stStr = stStr.rstrip('\r\n')
             val =int(stStr)
         except:
             inst.addToExcecptionList(sys.exc_info())
             return 0xfffffffd
    return val

   

def execCmd(inst,fileName,cmd,debugOn):
    if debugOn : 
       print cmd
    try :
        inst.ssh.sendline("echo "+cmdBannerFromat1+" >> "+fileName)
        inst.ssh.prompt()
        inst.ssh.sendline("echo "+cmdBannerFormat2 % cmd+" >> "+fileName)
        inst.ssh.prompt()
        inst.ssh.sendline(cmd+" >> "+fileName)
        inst.ssh.prompt()
    except:
        # if the there is problem while executing one command then we will not consider it as 
        # very critical . we will be adding the exception generated to exception list   
        inst.addToExcecptionList(sys.exc_info())
        return 0xffffffff

    val = getStatusOfCmdExec(inst)
    try :
        inst.ssh.sendline("echo "+cmdBannerFormat3+">>"+fileName)
        inst.ssh.prompt()
    except:
       # incase if we are not able to add the end banner then just ignore this error 
        pass 
    return val    

def executeCmdList(inst,fileName,lst,debugOn):
    count =0
    if debugOn == True :
       print "List of commands which will be excuted"
    res=[execCmd(inst,fileName,cmd,debugOn) for cmd in lst]
    return res 


def createSSHSession(inst,ip,uname,passwd,keyfile):
    ssh = pxssh.pxssh()
    try :
        ssh.login(ip,uname,passwd,ssh_key=keyfile)
    except :
        inst.addToExcecptionList(sys.exc_info())
        raise
    return ssh    
