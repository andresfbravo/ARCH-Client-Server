import zmq
import hashlib
import json
import os

#craacion de contexto parte del cliente
context = zmq.Context()

#creacion de socket
s = context.socket(zmq.REQ)
socket = context.socket(zmq.REQ)   
#asociacion de socket a ip del cliente
s.connect("tcp://127.0.0.1:9999")

sizePart = 1024*1024*5 
sizeBuf = 65536
file = {}

def upload(path):
	with open(path, 'rb') as f :
		sha256 = hashlib.sha256()
		while True: # generando hash del archivo
			data = f.read(sizeBuf)
			if not data :
				break
			sha256.update(data)

	file[os.path.basename(path)] = sha256.hexdigest()
	with open("datos.json", "w") as f:
		json.dump(file, f)
    # Submit File in the server
	name = sha256.hexdigest().encode()                            # File's hash
	socket.send_multipart([b"create", name])                    # Create File In server
	ans = socket.recv()

	with open(path, 'rb') as f :
		while True:
			data = f.read(sizeBuf)
			if not data :
				break
			socket.send_multipart([name, data])      # Send Data
            #print(data)
			ans = socket.recv()       
                          # The server forever Reply "OK"
	print(sha256.hexdigest())

with open("datos.json", "a+") as f:
    f.seek(0)
    data = f.read(1)
    if not data:
        f.write("{}")

with open("datos.json") as myfile:
    file = json.load(myfile)

while True:
    valor = input().split()
    print (valor[0])
    """
    if len(valor) != 2:
        print("No Esta Bien Escrito")
    else:
        if valor[0] in switcher:
            switcher[valor[0]](valor[1])
        else :
            print("esta mal escrito")
     """
    upload(valor[1])