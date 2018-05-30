import telnetlib
HOST = "192.168.1.1"
user = "root"
password = "sah"
LNX_prompt  = b'/cfg/system/root # '
 
        
tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
        
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"ls ")

ret1 = tn.read_until(LNX_prompt, 3)
print (ret1) #or use however you want

tn.write(b"exit\n")
     
