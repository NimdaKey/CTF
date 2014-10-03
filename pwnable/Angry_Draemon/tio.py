import telnetlib
import re

class tio:
    def __init__(self,host='127.0.0.1',port=23, timeout=30):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.io = telnetlib.Telnet(self.host, self.port, self.timeout)

    def send(self,data):
        return self.io.write(data)

    def read_until(self,data):
        return self.io.read_until(data)

    def read_until_re(self,pattern):
        content = self.io.read_all()
        return re.search(pattern, content)
        
    def close(self):
        self.io.close()
