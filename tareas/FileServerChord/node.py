import sys
import zmq
import json
import os
import hashlib
import re, uuid

"""
Registro=
	{
	hash_file : [parts in this server]
	}

Succesor=
	{
	"hash" : hash
	"ip": ip:port
	}
"""
sizePart = 1024*1024*10  #bytes
m = 256

class Node:
	def __init__(self):
		self.mac = str(uuid.getnode())
		hash_calc = hashlib.sha256()
		hash_calc.update(self.mac.encode())
		self.hash = str(hash_calc.hexdigest())
		self.successor = {}
		print(self.hash)

	def Start(self):
		print("\n-- Welcome to UltraServerChord¢2019 --\n")
		print("To initialize Chord provide the your ip,port and then a node ip:port for connect")
		print("\tpython3 node.py ip port<node> ip:port<ring> <folderName> \n")
		print("Example: python3 node.py 192.168.0.0 8001 127.255.255.0:8080 folder")

		if len(sys.argv) != 5:
			print("\n-- Error --\n")
			print("\tInvalid sintax")
			exit()

		ip=sys.argv[1]
		port=sys.argv[2]
		self.web=sys.argv[3]
		self.loc=sys.argv[4]
		self.register={}

		if os.path.isdir('./'+self.loc) == False:
			print("\nThis folder doesn't exist ")
			print("Creating the new directory /{}".format(self.loc))
			os.mkdir('./'+self.loc)

		#this is a first connection into two nodes
		# there is listening
		context = zmq.Context()
		self.socket = context.socket(zmq.REP)
		self.socket.bind("tcp://*:"+ port)

		# there is calling other nodes
		socket_s = context.socket(zmq.REQ) # socket al sucesor

		# if the web direction is the same of my ip address that means it's the first node
		if self.web == str(ip+":"+port):
			print("i am the first u.u")
			self.successor = {"hash":self.hash,"ip":str(ip+port)}
		else:
			socket_s.connect("tcp://" + self.web)
			socket_s.send_multipart([b"add_successor",self.hash.encode(),ip.encode(),port.encode()])
			response = socket_s.recv_multipart()

			while response[0].decode() == "this way":
				other_socket = eval(response[1].decode())
				print("Asking again to "+other_socket.get("hash")+":( ")

				#socket_s.connect("tcp://" + )
				#socket_s.send_multipart([b"add_successor", self.hash.encode(), ip.encode(), port.encode()])

			if response[0].decode() == "welcome":
				print("I know my place =D")
				#socket_s.send_multipart([b"set_successor",self.hash.encode(),ip.encode(),port.encode()])
				#recv_successor = self

		print ("Connecting to web now ...")
		while True:
			print("\nListening in "+ip+":"+port+" ...")
			query = self.socket.recv_multipart()
			if query[0].decode() == "add_successor":
				print("ask for new node\n"+query[1].decode()+"\nip "+query[2].decode()+":"+query[3].decode()+" O.O")
				req_successor={"hash":query[1].decode(),"ip":str(query[2].decode()+":"+query[3].decode())}
				x=int(self.hash, 16)
				y=int(query[1].decode(),16)
				z=int(self.successor.get("hash"), 16)
				print(x,y,z)
				if x > y and y < z :
					print ("this node comes here")
					self.socket.send_multipart(b"welcome")
				else:
					print ("this node is lose ")
					self.socket.send_multipart([b"this way",str(self.successor).encode()])

			if query[0].decode() == "successor":
				self.socket.send(self.successor.encode())

	def updateFinger(self):
		pass

"""
	def connect(self):
		contextP = zmq.Context()
		socketP = contextP.socket(zmq.REQ)
		#a = input()
		node = "tcp://" + self.ip_other_Node + ":" + self.port_other_Node
		socketN.connect(node)
		#   socketN.send_multipart([b"server",self.IP_SERVER.encode(),self.PORT_SERVER.encode(),str(self.f_space).encode()])
		req = socketP.recv()
		if req.decode()=="NEXT":
			socketP.send_json(self.register)

		response = socketN.recv()
		if response.decode()=="OK":
			print ("\nNodo is connected ")
		else:
			print("Error!")

"""

if __name__ == '__main__':
	Node = Node()
	Node.Start()
