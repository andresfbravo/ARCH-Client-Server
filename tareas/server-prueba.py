import zmq
import os

sizePart = 1024*1024*10  #bytes
context = zmq.Context()
socket = context.socket(zmq.REP) 
socket.bind("tcp://*:8000")
print("server on fire")
while True:
	print("bno")
	data = socket.recv_multipart()
	print(data)
	#socket.send(b"Recibido")
	print("bn")
