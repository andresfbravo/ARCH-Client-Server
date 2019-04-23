import zmq
import os

sizePart = 1024*1024*10  # 10MB
context = zmq.Context()
socket = context.socket(zmq.REP) # REP because is Reply
socket.bind("tcp://*:9999")

def upload(data) :
    name = data[1].decode()
    with open(name, "ab") as f:
        f.write(data[2])
    socket.send(b"OK")

print("Server ON")

while True:
	print("hola")
	hac = socket.recv_multipart()
	upload(hac)