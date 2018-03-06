import socket,pymysql
#setup
ip_add,port = "127.0.0.1",4000
ser_sd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ser_sd.bind((ip_add,port))
ser_sd.listen(5)
cli_sd,cli_add = ser_sd.accept()
#setup pymysql
db = pymysql.connect("localhost","root","123456","test")
cursor = db.cursor()
#
msg = "Enter Name\n> "
cli_sd.send(msg.encode('ascii'))
msg = cli_sd.recv(1024)
user_name = msg.decode('ascii')

sql = "select * from user where uname=\""+str(user_name)+"\";"
cursor.execute(sql)
rows = cursor.fetchall()
for i in rows:
	for j in range(3):
		print(i[j])
#
cli_sd.close()