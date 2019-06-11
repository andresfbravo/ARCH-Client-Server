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
PORT_SERVERS = "8000"

"""
main register
{
	sha256.decode():
		{
		"parts":[] 	#partes del archivo
		"loc":[]	#ip donde esta cada una
		}
}
"""
class Proxy:
	def Start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print("SYNTAX: python3 proxy.py <register> \n")
		print("\tTo initialize the proxy provide a file to register the servers")
		print("\t<register>\t register of contained files (will be create if doesn't exist)\n")
		print("\tThis file must be in the same folder of this file an you should called like an argument")
		print("\tExample: python3 proxy.py servers.json\n")

		self.main_register={}
		self.reg_file=sys.argv[1]

		if os.path.isfile('./'+self.reg_file) == False:
			print("\nThis register file doesn't exist ")
			print("Creating the new register /{}\n".format(self.reg_file))
			with open(self.reg_file,"x") as f: 	
				json.dump(self.main_register,f)
		else:	
			print("Register find\nCharging file ...\n")
			with open(self.reg_file) as read_file: 
				self.main_register=json.load(read_file)

		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind("tcp://*:"+PORT_SERVERS)
		print ("Proxy is now listening servers in port "+PORT_SERVERS)
		self.listening()
	
	def listening(self):
		self.register_server=[]
		while True:
			parts=[]
			print("\nListening ...\n")
			who,*rest = self.socket.recv_multipart()
			if who.decode()=="server":
				print("Welcome server: ")
				ip,port,parts = rest
				print(ip.decode(),port.decode(),parts.decode())
				nodo=ip.decode()+":"+port.decode()
				self.register_server.append(nodo)
				self.socket.send(b"OK")

			elif who.decode()=="client":
				print("Welcome client: ")
				operation,hash_file = rest
				print("Operation :"+operation.decode())
				if (hash_file.decode() in self.main_register):
					print("ya existe")
					self.socket.send(b"repeated")
				else:
					self.socket.send(b"OK")
					if operation.decode()=="upload":
						self.upload(hash_file)
					elif operation.decode()=="download":
						self.download(hash_file)
			print("Operation complete successfully!")
			#print(self.register_server)


	def upload(self,hash_file):
		print("Reciving parts ...")
		parts=self.socket.recv_json()
		self.main_register.update(parts)
		with open(self.reg_file, "w") as f:
			json.dump(self.main_register, f)
		print(self.main_register)
		
		n=len(self.main_register.get(hash_file.decode()).get('parts'))
		print("esto es n: "+str(n))
		#a = "192.168.9.1:8000"
		loc=[]
		x=0
		while x < n:
			for s in range(0,len(self.register_server)):
				loc.append(self.register_server[s])
			x=x+len(self.register_server)
		loc2=[x.encode() for x in loc]
		self.socket.send_multipart(loc2)
		#self.socket.send(b"OK")

	def download(self,hash_file):
		print("send parts ...")
		dicc = self.main_register.get(hash_file)
		self.socket.send(dicc.encode())

	

if __name__ == '__main__':
	Proxy = Proxy()
	Proxy.Start()
