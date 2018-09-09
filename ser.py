import socket,time,_thread,os
from db_conf import *
cursor = db_config()
#setup
ip_add,port = "",4002
ser_sd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ser_sd.bind((ip_add,port))
ser_sd.listen(5)

#cli_sd,cli_add = ser_sd.accept()#this goes in the thread


#
#global variables
defaultpath = "/home/vnit/users/"
noofthreads = 2

#---------------------------------------------------------------------------------------
def getnamepath(email):
	sql = "select name,path from user where email=\""+email+"\""
	cursor.execute(sql)
	rows = cursor.fetchall()
	#rows[0][0] = name
	#rows[0][1] = path
	return rows[0][0]+","+rows[0][1]

def addtodatabase(email,passw,name):
	path = name+"/";
	sql = "insert into user(email,password,name,path,id) values(\""+email+"\",\""+passw+"\",\""+name+"\",\""+path+"\",0)"
	if(cursor.execute(sql)):
		cursor.execute("commit")
		return True
	else:
		return False

def passwordchecker(email,passw):
	sql = "select password from user where email = \""+email+"\";"
	cursor.execute(sql)
	rows = cursor.fetchall()
	if(rows[0][0]==passw):
		return True
	else:
		return False


def validemailid(email,mode):
	if(("@" in email) and ("." in email)):
		if(mode=="r"):
			mode = 0
		elif(mode=="l"):
			mode = 1
		sql = "select email from user where email =\""+email+"\";";
		if(cursor.execute(sql)==mode):
			return True
		else:
			return False
	else:
		return False

#---------------------------------------------------------------------------------------
def func1(id):
	while(True):
		cli_sd,cli_add = ser_sd.accept()
		print("\nid : "+str(id))
		while(True):
			print("menu1 reached")
			text1 = cli_sd.recv(1024)
			text1 = text1.decode('ascii')
			#---------------------------------------------------------------------------------------
			if(text1=="login"):
				print("in login")
				access = 0
				while(access!=1):#email verification
					try:
						temp1 = cli_sd.recv(1024)#email
						temp1 = temp1.decode('ascii')

						if(validemailid(temp1,"l")):
							access = 1
							email_cli = temp1
							cli_sd.send(str("access").encode('ascii'))
						else:
							cli_sd.send(str("error").encode('ascii'))
					except:
						break

				if(passwordchecker(email_cli,cli_sd.recv(1024).decode('ascii'))):
					cli_sd.send("access".encode('ascii'))
					#password is verified
					maininterface(email_cli,cli_sd)
				else:
					cli_sd.send("error".encode('ascii'))



			#------------------------------------------------------------------------------------
			elif(text1=="register"):
				print("in register")
				var1 = False
				while(var1!=True):
					email_cli = cli_sd.recv(1024)
					email_cli = email_cli.decode('ascii')
					if(validemailid(email_cli,"r")):
						cli_sd.send("access".encode('ascii'))
						print("access sent")
						var1 = True
					else:
						print("error sent")
						cli_sd.send("error".encode('ascii'))#email is verified

				#recieve a password
				print("getting password")
				pass_cli = cli_sd.recv(1024).decode('ascii')
				print(pass_cli)

				#recieve a name
				print("getting name")
				name_cli = cli_sd.recv(1024).decode('ascii')

				#add all values to database
				if(addtodatabase(email_cli,pass_cli,name_cli)):
					cli_sd.send("access".encode('ascii'))
				else:
					cli_sd.send("error".encode('ascii'))

				#create folder
				os.mkdir("/home/vnit/users/"+name_cli)

			#---------------------------------------------------------------------------------------
			elif(text1=="exit"):
				#session[]
				print("id : "+str(id)+" closed\n")
				cli_sd.close()
				break
			#---------------------------------------------------------------------------------------

def maininterface(email,cli_sd):
	print("maininterface reached")
	cli_sd.send(getnamepath(email).encode('ascii'))#sending name and path
	while(True):
		print("maininterface menu selection")
		option = cli_sd.recv(1024).decode('ascii')
		if(option=="upload"):#upload
			print("in path")
			#receiving path
			path = cli_sd.recv(1024).decode('ascii')
			print(path)
			#receving filename
			filename = cli_sd.recv(1024).decode('ascii')
			filename = filename
			#file exists or not
			if(cli_sd.recv(6).decode('ascii')=="exists"):
				print("receving file")
				#receiving file size and format
				size,format = cli_sd.recv(1024).decode('ascii').split(",")
				cli_sd.send("abc".encode('ascii'))#temporary, has no use
				size = int(size) + 1
				contents = cli_sd.recv(size)
				#print(str(size)+" "+format+" "+contents.decode('ascii'))
				#receive file according to size
				if(format=="txt"):
					print("in txt")
					fp = open(path+filename,"w+")
					print(str(size)+" "+format+" "+contents.decode('ascii'))
					contents = contents.decode('ascii')
				elif(format=="jpg"):
					print(str(size)+" "+format+" "+str(contents))
					fp = open(path+filename,"wb")
				fp.write(contents)
				fp.close()
			else:
				print("in else")
				pass

		elif(option=="download"):#download
			print("in download")
			#receiving path
			path = cli_sd.recv(1024).decode('ascii')
			print("received path : "+path)
			#receiving filename
			filename = cli_sd.recv(1024).decode('ascii')
			print("received filename : "+filename)

			if(os.path.isfile(path+filename)):
				cli_sd.send("exists".encode('ascii'))
				if(".txt" in filename):
					fp = open(path+filename,"r")
					format = "txt"
					contents = fp.read()
					#sending file size
					cli_sd.send((str(len(contents))+","+str(format)).encode('ascii'))
					cli_sd.send(contents.encode('ascii'))
				elif(".jpg" in filename):
					fp = open(path+filename,"rb")
					format = "jpg"
					contents = fp.read()
					#sending file size
					cli_sd.send((str(len(contents))+","+str(format)).encode('ascii'))
					cli_sd.send(contents)
				print("reached end")
			else:
				cli_sd.send("nexists".encode('ascii'))

		elif(option=="list"):#list files
			path = cli_sd.recv(1024).decode('ascii')
			dirlist = ""
			for i in os.listdir(path):
				dirlist = dirlist + i +","
			dirlist = dirlist[0:len(dirlist)-1]
			print(dirlist)
			if(len(dirlist)==0):
				dirlist = "blank"
			cli_sd.send(dirlist.encode('ascii'))#sending dir list

		elif(option=="changedir"):#change directory
			print("in changedir")
			path = cli_sd.recv(1024).decode('ascii')
			if(os.path.isdir(path)):
				cli_sd.send("exists".encode('ascii'))
			else:
				cli_sd.send("nexists".encode('ascii'))

		elif(option=="logout"):#logout
			return

#---------------------------------------------------------------------------------------


try:
	for i in range(noofthreads):
		_thread.start_new_thread(func1,(int(i)+1,))
	# _thread.start_new_thread(func1,(1,))
	# _thread.start_new_thread(func1,(2,))
except:
	pass
'''
passw = cli_sd.recv(1024)
passw = passw.decode('ascii')
'''
'''
while(True):
	pass
'''
'''
msg = "Enter Name\n> "
cli_sd.send(msg.encode('ascii'))
msg = cli_sd.recv(1024)
user_name = msg.decode('ascii')

sql = "select * from user where uname=\""+str(user_name)+"\";"
cursor.execute(sql)
rows = cursor.fetchall()
for i in rows:
	for j in range(5):
		print(i[j])
'''
while(1):
	pass
#
#cli_sd.close()#in the thread
ser_sd.close()
