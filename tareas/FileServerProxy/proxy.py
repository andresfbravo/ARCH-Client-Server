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
	def start(self):
		os.system("clear")
		print("Proxy of ultraServer Running")

		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:"+PORT)
		print ("\tProxy is now runnig in port "+PORT)

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
