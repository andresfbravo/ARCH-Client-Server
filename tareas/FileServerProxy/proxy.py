import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
PORT_SERVERS = "8002"
ports={}

class Proxy:
	def Start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print("\tTo initialize the proxy provide the file whit the server list")
		print("\t Example: python3 proxy.py servers.json\n")

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
				print("welcome server: ")
				ip,port,parts=rest
				ports.update({parts:[ip,port]})
				print(ip.decode(),port.decode(),parts.decode())
				self.socket.send(b"OK") 
				
			elif who.decode()=="client":
				print("welcome client: "+rest)
				self.socket.send(b"OK") 



if __name__ == '__main__':
	Proxy = Proxy()
	Proxy.Start()
