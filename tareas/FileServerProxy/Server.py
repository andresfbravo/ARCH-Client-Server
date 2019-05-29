"""
Created on Tue Apr 16 2019
@author: Esteban Grisales
"""
import sys
import zmq
import json
import os
import time

sizePart = 1024*1024*10  #bytes
PORT = "8001"
register={}

class Server:
	def Start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print("\tTo initialize the server provide a folder for save the files")
		print("\t Example: python server.py <location>\n")

		if len(sys.argv) != 2:
			print("\n-- Error --\n")
			print("\tPlease call a folder name")
			exit()

		loc=sys.argv[1]
		if os.path.isdir('./'+loc) == False:
			print("This route doesn't exist ")
			print("Making new directory /{}".format(loc))
			os.mkdir('./'+loc)

		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:"+PORT)
		print ("\nServer is now runnig in port "+PORT)

		while True:
			print("\nListening...\n")
			sha256, ident, message,*rest = socket.recv_multipart()
			filename,info = rest
			register={"id":ident.decode(),"hash":sha256.decode(),"filename":filename.decode()}
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
		# fin start

	def upload(self, sha256, filename, info, socket, ident, loc) :

		#newName=loc+'/'+ident.decode()+'-'+filename.decode()
		newName = loc+'/'+sha256.decode()
		#print("Storing as [{}]".format(newName))
		with open(newName,"wb") as f:
			f.write(info)
		print("recibed")
		socket.send(b"OK")
		print("Send by [{}]".format(ident.decode()))
		print("File: [{}]".format(filename.decode()))
		time.sleep(5)
	def download(self, filename, socket, ident, loc):
		print(filename)
		fl=filename[0].decode()
		#newName="./"+folder+'/'+ident.decode()+"-"+fl
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
