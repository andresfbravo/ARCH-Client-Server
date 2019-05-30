import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
PORT_SERVERS = "8002"
PORT_CLIENTS = "8001"
servers=[]
register={}
regisUp={}

class Proxy:
	def Start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print("\tTo initialize the proxy provide the file whit the server list")
		print("\t Example: python3 proxy.py servers.json\n")

		if len(sys.argv) != 2:
			print("\n-- Error --\n")
			print("\tPlease call whit a json file")
			exit()

		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:"+PORT_SERVERS)
		print ("\tProxy is now listening servers in port "+PORT_SERVERS)
		
		self.register_file=sys.argv[1]

	

	def listening(self):
		while True:
			print("\nListening...\n")
			regisUp = socket.recv_json()

			print(register)
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
