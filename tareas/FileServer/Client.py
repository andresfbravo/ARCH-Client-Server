#ServerFile
#Client

import zmq
import json
import hashlib

#Se crea el contexto
context = zmq.Context()

#hago la creacion del socket solicitandolo al contexto
s = context.socket(zmq.REQ)#REQ debido a que va a hacer requerimientos de informacion
#conecto el socket a la tarjeta de red por defecto
ip = "tcp://127.0.0.1:5002"
s.connect(ip)
tamañoParte = 1024*1024*10  # 10MB
buff = 65536

