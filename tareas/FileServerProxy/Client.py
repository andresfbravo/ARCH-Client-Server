"""
Created on Tue May 09 2019
@author: Esteban Grisales && Andres Felipe Bravo
Arquitectura Cliente Servidor - UTP
"""
import zmq
import hashlib
import json
import os
import sys

sizePart = 1024*1024*10
ip="192.168.8.116"
PORT = "8002"
sizeBuf = 65536

class Client:
	def Start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print(".\tUse <id> <function> <route> to acces interface")
		print(".\t<id>\t  use the same id for all your consults")
		print(".\t<function> there is 2 options:\n\t   \"upload\"\n\t   \"download\"")
		print(".\t<route>\trute of the file, </home/images> \n")
		print(".\t<filename>\tthe name of the file <ejemplo.jpg> \n")

		if len(sys.argv) != 5:
			print("\n-- Error --\n")
			print("\tInvalid sintax, try again please")
			exit()

		self.ident= sys.argv[1].encode()
		self.operation = sys.argv[2].encode()
		self.route = sys.argv[3].encode()
		self.filename=sys.argv[4].encode()

		context = zmq.Context()
		self.socket_proxy = context.socket(zmq.REQ)
		self.socket_proxy.connect("tcp://"+ip+":"+PORT)
		self.proxy_negotiations()

	def proxy_negotiations(self):
		print("Establishing connection to proxy ...")
		self.socket_proxy.send_multipart([b"client", self.operation])
		response = self.socket_proxy.recv()
		if response.decode()=="OK":
			print("Proxy connected succesfully\n")
		else:
			print("Error conecting to proxy!")

		if self.operation.decode()=='upload':
		    self.upload_proxy()
		    #self.upload_server(self.socket_servers, self.ident)
		elif operation.decode()=='download':
			self.download(self.filename,self.socket_proxy,self.ident)
		print("Operation complete ")

	def upload_proxy(self):
		print("Making file parts for send ...")
		parts = []
		with open(self.route.decode()+self.filename.decode(), 'rb') as f:
			while True:
				byte = f.read(sizePart)
				if not byte:
					break
				sha2 = hashlib.sha256()
				sha2.update(byte)
				parts.append(sha2.hexdigest())

		print("Parts to send: ",len(parts))
		print("Preparing to send parts ...")
		register={self.get_hash().decode():{"parts":parts}}
		#register={"id":ident.decode(),"hash":sha256.decode(),"filename":filename.decode()}
		#with open("register.json", "a") as f:
			#json.dump(register, f)
		self.socket_proxy.send_json(register)
		#self.socket_servers.connect("tcp://"+ip+":"+PORT)
		#return {"filename" : sha256.hexdigest(),"parts" :parts}
		response = self.socket_proxy.recv_multipart()
		print(response)


	def upload_server(self):
		with open(self.route.decode()+self.filename.decode(), "rb") as f:
			finished = False
			part = 0
			while not finished:
				f.seek(part*sizePart)
				bt = f.read(sizePart)
				socket.send_multipart([self.get_hash(),self.ident, b"upload",self.filename, bt])
				response = socket.recv()
				if response.decode()=="repeated":
					print("The file already exists in server \n")
					finished = True
					break
				if len(bt) < sizePart:
					finished = True
				print("Uploading part {}".format(part+1))
				part+=1
				if response.decode()=="OK":
					print("Part send succesfully\n")
				else:
					print("Error!")

	def download(self,filename,socket,ID):
		#print("Download not implemented yet!!!!")
		socket.send_multipart([ID,b'download',filename])
		response=socket.recv_multipart()
		filename,info=response
		print("write[{}]".format(filename))
		self.writeBytes(filename.decode(),info)

	def writeBytes(self):
		newName='new-'+self.route
		print("Writing file...[{}]".format(newName))

		with open(newName,"wb") as f:
		    f.write(info)
		print("Downloaded [{}]".format(newName))

	def get_hash(self):
		with open(self.route.decode()+self.filename.decode(), 'rb') as f :
			sha256 = hashlib.sha256()
			while True:
				file = f.read(sizeBuf)
				if not file :
					break
				sha256.update(file)
		hashfile = sha256.hexdigest().encode()
		return hashfile

if __name__ == '__main__':
	Cliente = Client()
	Cliente.Start()
