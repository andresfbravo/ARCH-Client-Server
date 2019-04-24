import zmq
import os

sizePart = 1024*1024*10  #bytes
context = zmq.Context()
socket = context.socket(zmq.REP) 
socket.bind("tcp://*:9999")


def upload(data) :
	data = socket.recv_multipart()
	name = data[1]
	socket.send(b"Recibido")
	sha256 = data[2]
	print("Recibiendo archivo: ", name)
	while True:
		with open(name, "ab") as f:
			f.write(data[3])
		socket.send(b"Recibido")

while True:
	print("Fuego en el hoyo")
	hac = socket.recv_multipart()
	print(hac)
	break

#upload()