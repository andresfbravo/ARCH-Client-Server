import zmq

#craacion de contexto parte del cliente
context = zmq.Context()

#creacion de socket
socket = context.socket(zmq.REQ)   
#asociacion de socket a ip del cliente
socket.connect("tcp://127.0.0.1:8000")
print("conectado")
socket.send_multipart([b"hola"])
print("enviado")
