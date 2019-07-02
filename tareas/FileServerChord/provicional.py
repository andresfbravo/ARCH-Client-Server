def download(self):
	
	with open(newName, "rb") as f:			
		print("Downloading part {}".format(filename))
		bt = f.read(sizePart)
		print("prueba1")
		socket.send_multipart([bt])
		print("prueba2")
	res = socket.recv()
	if (res == "OK"):
		print("send successfully!!")
		
	#socket.send(b"OK")
	print("Downloaded!!")
	pass

def upload(self):
		sha256 = self.response[1]
		newName = self.loc+'/'+sha256.decode()
		with open(newName,"xb") as f:
			f.write(response[2])
		#socket.send(b"OK")