import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
PORT = "8002"
servers={}
tor={}

class Proxy:
	def start(self):
		os.system("clear")
		print("Proxy of ultraServer Running")

		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:"+PORT)
		print ("\nServer is now runnig in port "+PORT)

		while True:
			print("\nListening...\n")
			tor = socket.recv_multipart()
			#filename,info = rest
			tor = {"id":ident.decode(),"hash":sha256.decode(),"filename":filename.decode()}
			with open("register.json", "w") as f:
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

