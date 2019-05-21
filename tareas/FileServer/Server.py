"""
Created on Tue Apr 16 2019
@author: Esteban Grisales
"""
import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
PORT = "8001"

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
			ident, message,*rest = socket.recv_multipart()
			print("New request: %s" % message.decode())
			if message.decode()=='upload':
				print("Receiving file...")
				filename,info = rest
				newName=loc+'/'+ident.decode()+'-'+filename.decode()
				print("Storing as [{}]".format(newName))
				with open(newName,"wb") as f:
					f.write(info)
				socket.send(b"OK")
				print("Uploaded as [{}]".format(newName))
			elif message.decode()=="download":
				print("Operation: Download File...")
				filename=rest
				self.download(filename, socket, ident,loc)
			elif message.decode()=="bye":
				exit()
			print("Complete!")

	def download(filename, socket, ID, folder):
	    print(filename)
	    fl=filename[0].decode()
	    newName="./"+folder+'/'+ID.decode()+"-"+fl
	    print("Downloading [{}]".format(newName))
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

	def upload(self,data) :
		data = socket.recv_multipart()
		name = data[1]
		socket.send(b"Recibido")
		sha256 = data[2]
		print("Recibiendo archivo: ", name)
		while True:
			with open(name, "ab") as f:
				f.write(data[3])
			socket.send(b"Recibido")

if __name__ == '__main__':
	Server = Server()
	Server.Start()
