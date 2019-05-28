"""
Created on Tue Apr 16 2019
@author: Esteban Grisales
"""
import zmq
import hashlib
import json
import os
import sys

sizePart = 1024*1024*10
sizeBuf = 65536
PORT = "8002"
file = {}

class Client:
	def ___init__(self, ident, operation, route, filename, socket):
		pass

	def crearListaHash(self):
		sha256 = hashlib.sha256()
		partes = []
		with open(path + dir, "rb") as f:
			while True:
				byte = f.read(65534)
				if not byte:
					break

				sha2 = hashlib.sha256()
				sha2.update(byte)
				partes.append(sha2.hexdigest())

				sha256.update(byte)

		print("cantidad de trozos que genera el archivo para upload: ",len(partes))
        return {'hashfile' : sha256.hexdigest(),
                'trozos' :partes,
                'name' : dir}

	def Start(self):
		os.system("clear")
		print("\n\n-- Welcome to UltraServer¢2019 --\n")
		print("Use <id> <function> <route> to acces interface")
		print("\t<id> \n\t   Please use the same id for all your consults")
		print("\t<function> there is 2 options:\n\t   \"upload\"\n\t   \"download\"")
		print("\t<route>\n \t\trute of the file, </home/images> \n")
		print("\t<filename>\n \t\tthe name of the file <ejemplo.jpg> \n")
		print("##################################\n \t> ")

		if len(sys.argv) != 5:
			print("\n-- Error --\n")
			print("\tMust be called with a route")
			exit()

		self.ident= sys.argv[1].encode()
		self.operation = sys.argv[2].encode()
		self.route = sys.argv[3].encode()
		self.filename=sys.argv[4].encode()
		#print(filename)

		context = zmq.Context()
		self.socket = context.socket(zmq.REQ)
		self.socket.connect("tcp://localhost:"+PORT)
		print("Establishing connection...")

		if self.operation.decode()=='upload':
		    self.upload(self.filename,self.socket, self.ident)
		elif operation.decode()=='download':
			self.download(self.filename,self.socket,self.ident)

	def writeBytes(self,route,info):
		newName='new-'+route
		print("Writing file...[{}]".format(newName))

		with open(newName,"wb") as f:
		    f.write(info)
		print("Downloaded [{}]".format(newName))

	def upload(self, filename, socket, ID):
		with open(self.route.decode()+filename.decode(), 'rb') as f :
			sha256 = hashlib.sha256()
			while True:
				file = f.read(sizeBuf)
				if not file :
					break
				sha256.update(file)
		print(sha256)
		nombreArchivo = sha256.hexdigest().encode()

		with open(self.route.decode()+self.filename.decode(), "rb") as f:
			finished = False
			part = 0
			while not finished:
				print("Uploading part {}".format(part+1))
				f.seek(part*sizePart)
				bt = f.read(sizePart)
				socket.send_multipart([nombreArchivo,ID, b"upload",filename, bt])
				#print("Received reply [%s]" % (response))
				part+=1
				if len(bt) < sizePart:
					finished = True
			response = socket.recv()
			if response.decode()=='OK':
				print("Uploaded successfully!")
			else:
				print("Error!")

	def download(self,filename,socket,ID):
		#print("Download not implemented yet!!!!")
		socket.send_multipart([ID,b'download',filename])
		response=socket.recv_multipart()
		filename,info=response
		print("write[{}]".format(filename))
		self.writeBytes(filename.decode(),info)
"""
	#file[os.path.basename(path)] = sha256.hexdigest()
    with open("info.json", "w") as info:
        json.dump(file, info)
        name = os.path.basename(path).encode() # Nombre del archivo
    ans = socket.recv()
    print(ans)
    with open(path, 'rb') as f :
        while True:
            data = f.read(sizeBuf)
            if not data :
                break
            socket.send_multipart([name,sha256, data])      # Send Data
            ans = socket.recv() # The server forever Reply "OK"
            print(ans)
with open("info.json", "a+") as f:
    f.seek(0)
    data = f.read(1)
    if not data:
        f.write("{}")
with open("info.json") as myfile:
    file = json.load(myfile)
"""

if __name__ == '__main__':
	Cliente = Client()
	Cliente.Start()
