import socket,os,time
#setup
ip_add,port = "127.0.0.1",4001
ser_sd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ser_sd.connect((ip_add,port))
#

#global variables
defaultpath = "/home/vnit/users/"
#---------------------------------------------------------------------------------------

def animmenu(menu):
	pline = ""
	for i in range(len(menu)):
		for j in range(len(menu[i])):
			pline = pline + menu[i][j]
			print(pline)
			time.sleep(0.01)
			os.system("clear")
	print(pline,end="")
	#time.sleep(3)
#---------------------------------------------------------------------------------------

def maininterface(email):
	name,path = ser_sd.recv(1024).decode('ascii').split(',')
	print(name+" "+path)
	curdir = ""
	userdir = name+"/"
	while(True):
		#getting directory and username
		menu2 = ['\t\t\tWelcome to main interface','\n---------------------','\n1. Upload File','\n2. Download File','\n3. List Files','\n4. Change directory','\n5. Logout','\n---------------------','\nCurrent directory : ']
		animmenu(menu2)
		print(defaultpath+userdir+curdir)
		op = int(input("Select\n> "))

		#---------------------------------------------------------------------------------------

		if(op==1):#upload
			ser_sd.send("upload".encode('ascii'))
			#send path
			ser_sd.send((defaultpath+userdir+curdir).encode('ascii'))

			#sending filename
			filename = str(input("\nEnter name of the file\n> "))
			ser_sd.send(filename.encode('ascii'))
			if(os.path.isfile("/home/vnit/users/"+filename)):
				ser_sd.send("exists".encode('ascii'))
				if(".txt" in filename):
					fp = open("/home/vnit/users/"+filename,"r")
					format = "txt"
					contents = fp.read()
					#sending file size and format
					ser_sd.send((str(len(contents))+","+str(format)).encode('ascii'))
					ser_sd.recv(1024).decode('ascii')#has no use
					print("filename sent")
					ser_sd.send(contents.encode('ascii'))
				if(".jpg" in filename):
					fp = open("/home/vnit/users/"+filename,"rb")
					format = "jpg"
					contents = fp.read()
					#sending file size and format
					ser_sd.send((str(len(contents))+","+str(format)).encode('ascii'))
					ser_sd.recv(1024).decode('ascii')#has no use
					print("filename sent")
					ser_sd.send(contents)
			else:
				ser_sd.send("nexists".encode('ascii'))
				print("File doesn't exist")
			time.sleep(3)



		#---------------------------------------------------------------------------------------

		elif(op==2):#download
			ser_sd.send("download".encode('ascii'))

			#sending path
			ser_sd.send((defaultpath+userdir+curdir).encode('ascii'))

			#send a filename
			filename = input("Enter a file to download\n> ")
			ser_sd.send(filename.encode('ascii'))
			#file exists or not
			if(ser_sd.recv(1024).decode('ascii')=="exists"):
				#receiving size of the file and format
				filesize,format = ser_sd.recv(1024).decode('ascii').split(',')
				filesize = int(filesize) + 1
				#receiving file according to size
				if(format=="txt"):
					contents = ser_sd.recv(filesize).decode('ascii')
					fp = open("/home/vnit/users/"+filename,"w+")
				elif(format=="jpg"):
					contents = ser_sd.recv(filesize)
					fp = open("/home/vnit/users/"+filename,"wb")
				fp.write(contents)
				fp.close()
			else:
				print("File does not exist")
				time.sleep(3)

		#---------------------------------------------------------------------------------------
		elif(op==3):#list files
			ser_sd.send("list".encode('ascii'))

			#sending the path
			ser_sd.send((defaultpath+userdir+curdir).encode('ascii'))
			print("List of files and folders")
			#getting list
			dir1 = list(ser_sd.recv(1024).decode('ascii').split(','))
			if(dir1[0]=="blank"):
				print("blank")
			else:
				for i in dir1:
					print(i)
			input("\n>")
		#---------------------------------------------------------------------------------------
		elif(op==4):#change directory
			ser_sd.send("changedir".encode('ascii'))

			curdir = input("Enter path\n> "+userdir)+"/"
			#sending the path
			ser_sd.send((defaultpath+userdir+curdir).encode('ascii'))
			if("../" in curdir):
				curdir = curdir[:len(curdir)-3]
			#file exists or not
			if(ser_sd.recv(1024).decode('ascii')=="exists"):
				pass
			else:
				curdir = ""
				print("Directory does not exist")
				time.sleep(2)
		#---------------------------------------------------------------------------------------
		elif(op==5):#logout
			ser_sd.send("logout".encode('ascii'))
			return

#---------------------------------------------------------------------------------------

menu1 = ['\t\t\tCentral Repository','\nMenu','\n---------------------','\n1. Login','\n2. Register','\n3. Exit','\n---------------------\n'] #menu

while(True):
	# for i in menu1:
	# 	print(i)
	animmenu(menu1)
	option = input("\n> ")
#---------------------------------------------------------------------------------------
	if(option=="1" or option=="Login" or option=="login"):
		print("Login selected")
		text1 = "login"
		ser_sd.send(text1.encode('ascii'))

		var1 = False
		while(var1 == False):
			email = input("Enter E-mail Id\n> ")
			ser_sd.send(email.encode('ascii'))
			reply = ser_sd.recv(1024)
			if(str(reply.decode('ascii'))=="error"):
					os.system("clear")
					print("Email does not exist/Invalid email/nTry again")
			else:
					var1 = True
					print("Approved")
		#email has been approved
		ser_sd.send(input("Enter password\n> ").encode('ascii'))
		if(ser_sd.recv(1024).decode('ascii')=="access"):
			print("Approved\n")
			maininterface(email)
		else:
			print("Wrong password\nTry again")

#---------------------------------------------------------------------------------------
	elif(option=="2" or option=="Register" or option=="register"):
		print("Register selected")
		text1 = "register"
		ser_sd.send(text1.encode('ascii'))
		var1 = False
		while(var1!=True):
			#send email
			ser_sd.send(input("Enter email\n> ").encode('ascii'))
			if(ser_sd.recv(1024).decode('ascii')=="access"):
				#send password
				ser_sd.send(input("Enter password\n> ").encode('ascii'))

				#send name
				ser_sd.send(input("Enter a username\n> ").encode('ascii'))
				var1 = True
			else:
				print("Try Again\nInvalid Email\Already exists\n")
		#all values sent
		if(ser_sd.recv(1024).decode('ascii')):
			print("All values sent")
		else:
			print("There was an error\nTry again\n")
#---------------------------------------------------------------------------------------
	elif(option=="3" or option=="Exit" or option=="exit"):
		print("exit")
		text1 = "exit"
		ser_sd.send(text1.encode('ascii'))
		exit(0)

	else:
		print("Wrong input")
#---------------------------------------------------------------------------------------

#
'''
msg = ser_sd.recv(1024)
print(msg.decode('ascii'),end="")
msg = input()
ser_sd.send(msg.encode('ascii'))
print("")
'''
#
ser_sd.close()
