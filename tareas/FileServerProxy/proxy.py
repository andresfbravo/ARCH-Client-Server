import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
PORT_SERVERS = "8002"
register_server=[]
"""
{ip+":"+port:espacio}}
"""

"""
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
		self.main_register={}
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print(".SYNTAX: python3 proxy.py <register> \n")
		print(".\tTo initialize the proxy provide a file to register the servers")
		print(".\t<register>\t register of contained files (will be create if doesn't exist)\n")
		print(".\tThis file must be in the same folder of this file an you should called like an argument")
		print(".\tExample: python3 proxy.py servers.json\n")

		self.reg_file=sys.argv[1]
		if os.path.isfile('./'+self.reg_file) == False:
			print("\nThis register file doesn't exist ")
			print("Creating the new register /{}".format(self.reg_file))
			with open(self.reg_file,"x") as f: 	
				json.dump(self.main_register,f)
		else:	
			with open('./'+self.reg_file) as k: 
				self.main_register=json.load(k)	

		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind("tcp://*:"+PORT_SERVERS)
		print ("\tProxy is now listening servers in port "+PORT_SERVERS)
		self.listening()
	
	def listening(self):
		while True:
			parts=[]
			print("\nListening ...\n")
			who,*rest = self.socket.recv_multipart()
			if who.decode()=="server":
				print("Welcome server: ")
				ip,port,parts = rest
				print(ip.decode(),port.decode(),parts.decode())
				nodo=ip.decode()+":"+port.decode()
				register_server.append(nodo)
				"""
				self.socket.send(b"NEXT") 
				json_server = self.socket.recv_json()
				#register_server=json.load(json_server)
				#print(json_server)
				"""
				#register_server.update({[ip,port]:[hash_file,hash_parts]})

				self.socket.send(b"OK")

			elif who.decode()=="client":
				print("Welcome client: ")
				operation,hash_file = rest
				print(rest)
				self.socket.send(b"OK")
				if operation.decode()=="upload":
					self.upload(hash_file)
				#elif operation.decode()=="download":
				#	for in range
			print("Operation complete successfully!")


	def upload(self,hash_file):
		print("vamos a ver")
		parts=self.socket.recv_json()
		self.main_register.update(parts)
		with open(self.reg_file, "a") as f:
			json.dump(self.main_register, f)
		print("prueba de fuego")
		print(self.main_register)
		#self.socket.send(b"OK")
		
		n=len(self.main_register.get(hash_file.decode()).get('parts'))
		print("esto es n: "+str(n))
		a = "192.168.9.1:8000"
		loc=[]
		for s in range(0,n):
			loc.append(a)
		loc2=[x.encode() for x in loc]
		self.socket.send_multipart(loc2)

	

if __name__ == '__main__':
	Proxy = Proxy()
	Proxy.Start()
