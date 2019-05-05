#This software is wearing zmq and this sw is running on python3.7
#FileServer
#Server
import zmq
import json

#Se crea el contexto
context = zmq.Context()

#hago la creacion del socket solicitandolo al contexto
s = context.socket(zmq.REP)#REP debido a que va a hacer replicas, "Enviar info"
#conecto el socket a la tarjeta de red por defecto
ip = 'tcp://*:5002'
s.bind(ip)
#Esta funcion recibe las partes enviadas por el cliente y las guarda en el servidor
def upload(archivo):
	nombre = archivo[1]
	with open(name, ab) as b:
		b.write(archivo[2])
	s.send(b"recibido completo")

print("El servidor de sumas esta corriendo en la ip: ", ip)
#Escucha todo el tiempo
while True:
	archivo = s.recv_multipart()#recibe todas las partes y las pone en en la variable archivo
	upload(archivo)

	
	#m="archivo"
	#s.send(m.encode('utf-8'))
