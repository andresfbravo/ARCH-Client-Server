	#ServerSuma
import zmq
import json

#Se crea el contexto
context = zmq.Context()

#hago la creacion del socket solicitandolo al contexto
s = context.socket(zmq.REP)#REP debido a que va a hacer replicas, "Enviar info"
#conecto el socket a la tarjeta de red por defecto
s.bind('tcp://*:5002')

print("El servidor de sumas esta corriendo")

while True:
	op, a1, a2 = s.recv_multipart()#recibe todas las partes y las pone en cada una de las variables
	print("operacion a realizar: ",op,"numero1: ",a1,"numero2: ",a2)

	#if(op=="+"):
	m="algo"
	s.send(m.encode('utf-8'))
