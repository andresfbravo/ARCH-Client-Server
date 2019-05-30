import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
PORT_SERVERS = "8002"
PORT_CLIENTS = "8001"
servers={"ip":[],"port":[]}
register={}
regisUp={}

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
	"""
		self.context_cl = zmq.Context()
		self.socket_cl = self.context_cl.socket(zmq.REP)
		self.socket_cl.bind("tcp://*:"+PORT_CLIENTS)
		print ("\tProxy is now listening clients in port "+PORT_CLIENTS)
		print ("#############################\n")
		#self.register_file=sys.argv[1]
	"""
	def listening(self):
		while True:
			#info = self.socket_cl.recv_multipart()
			#print("\nListening clients\n")
			print("\nListening servers\n")
			ip,port = self.socket.recv_multipart()
			print("Conecting server...\n")
			servers["ip"].append(ip.decode())
			servers["port"].append(port.decode())
			self.socket.send(b"OK")  
			print("New server connected: " + ip.decode() +":"+port.decode())
			print(servers)

			"""
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
			"""

if __name__ == '__main__':
	Proxy = Proxy()
	Proxy.Start()
