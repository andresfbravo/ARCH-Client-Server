"""
Created on Tue May 09 2019
@author: Esteban Grisales && Andres Felipe Bravo
Arquitectura Cliente Servidor - UTP 
"""
import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
IP_PROXY = "192.168.9.81"#"192.168.9.201"
PORT_PROXY = "8000"
"""{sha256.decode():
	{"id":id.decode(),
	"fnm":filename.decode(),
	"parts":[]
	}}
"""
class Server:
	def Start(self):
		self.f_space = 1000
		os.system("clear")
		print("-- Welcome to UltraServer¢2019 --\n")
		print("SYNTAX: python3 Server.py <folder> <ip> <port> <register> \n")
		print(" <folder>\t name of folder to save files (will be create if doesn't exist)")
		print(" <ip> <port>\t ip and port of the local machine")
		print(" <register>\t register of contained files (will be create if doesn't exist)\n")
		print(" Example: python server.py main_folder 192.168.0.2 8001 register.json \n")

		if len(sys.argv) != 5:
			print("\n-- Error --\n")
			print("\tInvalid sintax")
			exit()

		self.register={}
		self.reg_file=sys.argv[4]	
		self.PORT_SERVER=sys.argv[3]	
		self.IP_SERVER=sys.argv[2]
		self.loc=sys.argv[1]

		if os.path.isdir('./'+self.loc) == False:
			print("\nThis folder doesn't exist ")
			print("Creating the new directory /{}".format(self.loc))
			os.mkdir('./'+self.loc)

		if os.path.isfile('./'+self.reg_file) == False:
			print("\nThis register file doesn't exist ")
			print("Creating the new register /{}".format(self.reg_file))
			with open(self.reg_file,"x") as f: 	
				json.dump(self.register,f)
		else:	
			with open(self.reg_file) as k: 
				self.register=json.load(k)

		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:"+self.PORT_SERVER)
		print ("\nServer is now runnig in port "+self.PORT_SERVER)
		Server.connectToProxy()	
		Server.listen_clients(socket)		

	def connectToProxy(self):
		contextP = zmq.Context()
		socketP = contextP.socket(zmq.REQ)
		#a = input()
		PROXY = "tcp://" + IP_PROXY + ":" + PORT_PROXY
		socketP.connect(PROXY)
		socketP.send_multipart([b"server",self.IP_SERVER.encode(),self.PORT_SERVER.encode(),str(self.f_space).encode()])
		"""req = socketP.recv()
		if req.decode()=="NEXT":
			socketP.send_json(self.register)
		"""
		response = socketP.recv()
		if response.decode()=="OK":
			print ("\nServer is now connected with Proxy by the port "+PORT_PROXY)
		else:
			print("Error!")

	def listen_clients(self, socket):
		while True:
			print("\nListening clients...\n")
			sha256, ident, operation,*rest = socket.recv_multipart()
			#register.update({sha256.decode})
			print("New request: %s" % operation.decode())
			

			if operation.decode()=="upload":
				filename, file = rest
				data={}
				self.register.update({sha256.decode():{"id":ident.decode(),"fnm":filename.decode(),"parts":[]}})
				with open(self.reg_file, "w") as f:
					json.dump(self.register, f)
				self.upload(sha256, filename, file, socket, ident)
			
			if operation.decode()=="download":
				print("Part request: {}".format(sha256.decode()))
				
				#print(sha256.decode())
				name = self.register.get(sha256.decode()).get("fnm")
				print("File name: {}".format(name))
				socket.send(name.encode())
				self.download(sha256, socket, ident)
			elif operation.decode()=="bye":
				exit()
			print("Operation complete successfully!")

	def getCapacity(self):
		return self.f_space

	def upload(self, sha256, filename, file, socket, ident) :
		newName = self.loc+'/'+sha256.decode()
		#print("Storing as [{}]".format(newName))
		with open(newName,"xb") as f:
			f.write(file)
			self.f_space=self.f_space-1
		socket.send(b"OK")  
		print("[{} send {}]".format(ident.decode(),filename.decode()))

	def download(self, sha256, socket, ident):
		print("probando")
		filename = sha256.decode()
		print("filename is: ")
		print(filename)
		print("ya fue!!")
		newName=self.loc+'/'+sha256.decode()
		#print("Downloading [{}]".format(newName))
		print("Send by [{}]".format(ident.decode()))
		with open(newName, "rb") as f:			
			print("Downloading part {}".format(filename))
			bt = f.read()
			socket.send_multipart([bt])
		res = socket.recv()
		if (res == "OK"):
			print("send successfully!!")
			

		print("Downloaded!!")

if __name__ == '__main__':
	Server = Server()
	Server.Start()
	#Server.connectToProxy()
