import socket
#setup
ip_add,port = "127.0.0.1",4000
ser_sd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ser_sd.connect((ip_add,port))
#
msg = ser_sd.recv(1024)
print(msg.decode('ascii'))
msg = input()
ser_sd.send(msg.encode('ascii'))
#
ser_sd.close()