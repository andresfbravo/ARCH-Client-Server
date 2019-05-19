#ServerFile
#Client

import zmq
import json
import hashlib

print("<option> File")
print("submit pathFile")
print("download File")
print("add hash")
#Se crea el contexto
context = zmq.Context()

#hago la creacion del socket solicitandolo al contexto
s = context.socket(zmq.REQ)#REQ debido a que va a hacer requerimientos de informacion
#conecto el socket a la tarjeta de red por defecto
#ip = "tcp://127.0.0.1:5002"
s.connect("tcp://127.0.0.1:5002")
tamañoParte = 1024*1024*10  # 10MB
buff = 65536
Archivo={}

def upload(path):
	#le saco el hash al archivo y lo guardo en este server
	with open(path, 'rb') as f :
		sha1 = hashlib.sha1()
		while True:
			data = f.read(sizeBuf)
			if not data :
				break
			sha1.update(data)	
	#
	Files[os.path.basename(path)] = sha1.hexdigest()
	with open("datos.json", "w") as f:
		json.dump(Files, f)
		# Submit File in the server
		name = sha1.hexdigest().encode()                            # File's hash
		socket.send_multipart([b"create", name])                    # Create File In server
		ans = socket.recv()



"""
msj=[b"hola",b"claro"]
s.send_multipart(msj)
res=s.recv()
print("el servidor dice que: ",res.decode('utf-8'))
"""

switcher = { "submit" : upload, "download" : download, "add" : add}

with open("datos.json", "a+") as f:
    f.seek(0)
    data = f.read(1)
    if not data:
        f.write("{}")

with open("datos.json") as myFiles:
    Files = json.load(myFiles)

while True:
    valor = input().split()
    if len(valor) != 2:
        print("No Esta Bien Escrito")
    else:
        if valor[0] in switcher:
            switcher[valor[0]](valor[1])
        else :
            print("esta mal escrito")