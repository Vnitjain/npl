import socket
ip_add,port = "127.0.0.1",4000
ser_sd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ser_sd.bind((ip_add,port))
ser_sd.listen(5)
cli_sd,cli_add = ser_sd.accept()
msg = "Enter Name\n> "
cli_sd.send(msg.encode('ascii'))
cli_sd.close()