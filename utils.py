#!/usr/bin/python

from pexpect import spawn,TIMEOUT,EOF 
import sys
import signal 
decryptFormat = "openssl aes-256-cbc -d -in %s -out %s "
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
   
