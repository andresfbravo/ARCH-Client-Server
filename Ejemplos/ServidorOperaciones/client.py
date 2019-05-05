#cliene suma
import zmq
import json

context= zmq.Context()

s = context.socket(zmq.REQ)

s.connect("tcp://127.0.0.1:5002")

msj = [ b"+", b"3", b"4"]

s.send_multipart(msj)

res = s.recv()

print("respuesta del servidor", res.decode('utf-8'))