import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
PORT = "8002"
servers=[]
register={}
regisUp={}

class Proxy:
	def Start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print("\tTo initialize the proxy provide the file whit the server list")
		print("\t Example: python proxy.py <servers.json>\n")

		if len(sys.argv) != 2:
			print("\n-- Error --\n")
			print("\tPlease call a json file")
			exit()

		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:"+PORT)
		print ("\tProxy is now runnig in port "+PORT)
		self.register_file=sys.argv[1]

	def run_servers(self):
	with open('data.json') as file:
	    data = json.load(file)

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
