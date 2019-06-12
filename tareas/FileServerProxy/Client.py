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
ip="localhost"
PORT = "8000"
sizeBuf = 65536

class Client:
	def Start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print("Use <id> <function> <route> to acces interface")
		print("<id>\t  use the same id for all your consults")
		print("<function> there is 2 options:\n\t   \"upload\"\n\t   \"download\"")
		print("<route>\trute of the file, </home/images> \n")
		print("<filename>\tthe name of the file <ejemplo.jpg> \n")

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
		self.socket_proxy.send_multipart([b"client", self.operation, self.get_hash()])
		response = self.socket_proxy.recv()
		if response.decode()=="OK":
			print("Proxy connected succesfully\n")
			if self.operation.decode()=='upload':
				if response.decode()=="repeated":
					print("Proxy connected succesfully\n")
					print("This file already exists")
				self.upload_proxy()
				self.upload_server()
			elif self.operation.decode()=='download':
				self.download()

		print("Operation complete ")

	def upload_proxy(self):
		print("Making file parts for send ...")
		self.parts = []
		with open(self.route.decode()+self.filename.decode(), 'rb') as f:
			while True:
				byte = f.read(sizePart)
				if not byte:
					break
				sha2 = hashlib.sha256()
				sha2.update(byte)
				self.parts.append(sha2.hexdigest())

		print("Parts to send: ",len(self.parts))
		print("Preparing to send parts ...")
		register={self.get_hash().decode():{"parts":self.parts}}
		#register={"id":ident.decode(),"hash":sha256.decode(),"filename":filename.decode()}
		#with open("register.json", "a") as f:
			#json.dump(register, f)
		self.socket_proxy.send_json(register)
		#self.socket_servers.connect("tcp://"+ip+":"+PORT)
		#return {"filename" : sha256.hexdigest(),"parts" :parts}
		self.list_servers = self.socket_proxy.recv_multipart()
		self.register = []
		for x in range(0,len(self.parts)):
			self.register.append({self.parts[x]:self.list_servers[x].decode()})
		print(self.register)

	def upload_server(self):
		context2 = zmq.Context()
		with open(self.route.decode()+self.filename.decode(), "rb") as f:
			finished = False
			part = 0
			while not finished:
				self.socket_servers = context2.socket(zmq.REQ)
				self.socket_servers.connect("tcp://"+self.list_servers[part].decode())
				f.seek(part*sizePart)
				bt = f.read(sizePart)
				self.socket_servers.send_multipart([(self.parts[part]).encode(),self.ident,b"upload",self.filename, bt])
				response = self.socket_servers.recv()

				if len(bt) < sizePart:
					finished = True
				print("Uploading part {}".format(part+1))
				part+=1
				if response.decode()=="OK":
					print("Part send succesfully\n")
					self.socket_servers.close()
				else:
					print("Error!")


	def download(self):
		context2 = zmq.Context()
		self.socket_proxy.send(self.filename)
		list_hash = self.socket_proxy.recv_json()
		reg_down = json.loads(list_hash) 	# lista obtenida del proxy
		print(reg_down)
		print("Conecting to servers ...")
		parts = reg_down.get("parts")
		servers = reg_down.get("loc")
		self.socket_servers = context2.socket(zmq.REQ)
		for i in range(0,len(parts)):
			self.socket_servers.connect("tcp://"+servers[i])
			self.socket_servers.send_multipart([(parts[i]).encode(),self.ident,b"download"])
			Filename, bt = self.socket_servers.recv_multipart()
			with open(self.route.decode()+"/"+Filename.decode(), "ab") as f:
				self.socket_servers = context2.socket(zmq.REQ)
				self.socket_servers.connect("tcp://"+servers[i])
				f.seek(i*sizePart)
				f.write(bt)
				self.socket_servers.send(b"OK")
				self.socket_servers.close()
				print("Part download succesfully\n")

	def get_hash(self):
		if self.operation.decode() == "upload":
			with open(self.route.decode()+self.filename.decode(), 'rb') as f :
				sha256 = hashlib.sha256()
				while True:
					file = f.read(sizeBuf)
					if not file :
						break
					sha256.update(file)
			hashfile = sha256.hexdigest().encode()
			return hashfile
		elif self.operation.decode() == "download":
			return self.filename

if __name__ == '__main__':
	Cliente = Client()
	Cliente.Start()
