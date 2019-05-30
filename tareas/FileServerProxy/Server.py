"""
Created on Tue Apr 16 2019
@author: Esteban Grisales && Andres Felipe Bravo
Arquitectura Cliente Servidor - UTP 
"""
import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
partes = 1000
IP_PROXY = "192.168.1.12"
PORT_PROXY = "8002"
#PORT_CLIENTS = "8003"
register={}

class Server:
	def Start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print("\tTo initialize the server provide a folder for save the files")
		print("\t Example: python server.py <location> <IP> <PORT>\n")

		if len(sys.argv) != 4:
			print("\n-- Error --\n")
			print("\tPlease call a folder name")
			exit()

		self.PORT_SERVER=sys.argv[3]
		#if os.path.isdir('./'+PORT) == False:
			#print("This route doesn't exist ")
			#print("Making new directory /{}".format(loc))
			#os.mkdir('./'+loc)

		self.IP_SERVER=sys.argv[2]
		#if os.path.isdir('./'+IP) == False:
		#print("This route doesn't exist ")
		#print("Making new directory /{}".format(IP))
			#os.mkdir('./'+PORT)

		loc=sys.argv[1]
		if os.path.isdir('./'+loc) == False:
			print("This route doesn't exist ")
			print("Making new directory /{}".format(loc))
			os.mkdir('./'+loc)

		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:"+self.PORT_SERVER)
		print ("\nServer is now runnig in port "+self.PORT_SERVER)
		print("ya casi")
		Server.connectToProxy()	
		print("ehhh")
		while True:
			print("\nListening...\n")
			sha256, ident, message,filename, info = socket.recv_multipart()
			register={"id":ident.decode(),"hash":sha256.decode(),"filename":filename.decode()}
			with open("register.json", "a") as f:
				json.dump(register, f)

			print("New request: %s" % message.decode())
			if message.decode()=='upload':
				self.upload(sha256, filename, info, socket, ident, loc)
			elif message.decode()=="download":
				filename,info=rest
				print("File: [{}]".format(filename.decode()))
				self.download(filename, socket, ident, loc)
			elif message.decode()=="bye":
				exit()
			print("Complete!")
		# fin start

	def connectToProxy(self):
		contextP = zmq.Context()
		socketP = contextP.socket(zmq.REQ)
		#a = input()
		PROXY = "tcp://" + IP_PROXY + ":" + PORT_PROXY
		socketP.connect(PROXY)
		socketP.send_multipart([self.IP_SERVER.encode(),self.PORT_SERVER.encode()])
		response = socketP.recv()
		print(response.decode())
		if response.decode()=="OK":
			print ("\nServer is connected with Proxy by the port "+PORT_PROXY)
		else:
			print("Error!")

	def upload(self, sha256, filename, info, socket, ident, loc) :

		newName = loc+'/'+sha256.decode()
		#print("Storing as [{}]".format(newName))
		with open(newName,"ab") as f:
			f.write(info)
		socket.send(b"OK")  
		print("[{} send {}]".format(ident.decode(),filename.decode()))

	def download(self, filename, socket, ident, loc):
		print(filename)
		fl=filename[0].decode()
		newName=loc+'/'+sha256.decode()
		print("Downloading [{}]".format(newName))
		print("Send by [{}]".format(ident.decode()))
		with open(newName, "rb") as f:
			finished = False
			part = 0
			while not finished:
				print("Uploading part {}".format(part+1))
				f.seek(part*partSize)
				bt = f.read(partSize)
				socket.send_multipart([fl.encode(), bt])
				part = part + 1
			if len(bt) < partSize:
				finished = True

		print("Downloaded!!")

if __name__ == '__main__':
	Server = Server()
	Server.Start()
	#Server.connectToProxy()
