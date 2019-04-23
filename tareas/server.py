import zmq
import os

sizePart = 1024*1024*5  # 10MB
context = zmq.Context()
socket = context.socket(zmq.REP) # REP because is Reply
socket.bind("tcp://*:9999")

def upload(data) :
    name = data[1]
    sha256 = data[2]
    print("Recibiendo archivo: ", name)
    with open(name, "ab") as f:
        f.write(data[3])
    socket.send(b"Recibido")

print("Fuego en el hoyo")

while True:
    print("hola")
    hac = socket.recv_multipart()
    upload(hac)