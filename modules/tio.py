import telnetlib
import struct
import re

class tio(telnetlib.Telnet):
    def __init__(self,host='127.0.0.1',port=23, timeout=30):
        self.io=telnetlib.Telnet.__init__(self,host,port,timeout)

    def send(self,data):
        return self.io.write(data)

    def read_until_re(self,pattern):
        content = self.io.read_all()
        return re.search(pattern, content)
        
def l32(data):
    return struct.pack("<I",data)

def l64(data):
    return struct.pack("<Q",data)

def b32(data):
    return struct.pack(">I",data)

def b64(data):
    return struct.pack(">Q",data)
        
'''
# usage:

from tio import *

f=tio("192.168.2.107", 8888)

print f.read_until("Give up")
f.send("4\n")
f.read_until(") ")
f.send("y234567890\n")
token = f.read_until_re(r"y234567890\n(...)").group(1)
token = "\x00" + token
f.close()
print "Got canary:", token.encode("hex")
'''
