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
PORT = "8001"
file = {}

class Client:
	def Start(self):
		os.system("clear")
		print("\n\n-- Welcome to UltraServer¢2019 --\n")
		print("Use <id> <function> <filename> to acces interface")
		print("\t<id> \n\t   Please use the same id for all your consults")
		print("\t<function> there is 2 options:\n\t   \"upload\"\n\t   \"download\"")
		print("\t<filename>\n \t\tif it is in the path <ejemplo.jpg>, </home/images/ejemplo.jpg> other way\n")

		if len(sys.argv) != 4:
			print("\n-- Error --\n")
			print("\tMust be called with a filename")
			exit()

		ident= sys.argv[1].encode()
		operation = sys.argv[2].encode()
		filename = sys.argv[3].encode()

		context = zmq.Context()
		socket = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:"+PORT)
		print("Establishing connection...")

		if operation.decode()=='upload':
		    self.upload(filename,socket, ident)
		elif operation.decode()=='download':
			self.download(filename,socket,ident)
			"""
	def upload(path): # Subir archivo al servidor
		print("buscando archivo...")
		with open(path, 'rb') as f :
			sha256 = hashlib.sha256()
		print (sha256)
		while True: # generando hash del archivo
		data = f.read(sizeBuf)
		if not data :
			break
		sha256.update(data)
		"""
	def writeBytes(filename,info):
		newName='new-'+filename
		print("Writing file...[{}]".format(newName))

		with open(newName,"wb") as f:
		    f.write(info)
		print("Downloaded [{}]".format(newName))

	def upload(filename, socket, ID):
	    with open(filename, "rb") as f:
	        finished = False
	        part = 0
	        while not finished:
	            print("Uploading part {}".format(part+1))

	            f.seek(part*partSize)
	            bt = f.read(partSize)
	            socket.send_multipart([ID, b"upload",filename, bt])

	            #print("Received reply [%s]" % (response))
	            part+=1
	            if len(bt) < partSize:
	                finished = True
	        response = socket.recv()
	        if response.decode()=='OK':
	            print("Uploaded successfully!")
	        else:
	            print("Error!")

	def download(filename,socket,ID):
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
