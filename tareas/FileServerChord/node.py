import sys
import zmq
import json
import os
import hashlib


#sizePart = 1024*1024*10  #bytes

class Node:
	def start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServerChord¢2019 --\n")
		print("SYNTAX: python3 node.py location ip_Other_Node port_other_Node register.json \n")
		print("\tTo initialize Chord provide ")
		print("\tThis file must be in the same folder of this file an you should called like an argument")
		

		self.register = {}
		
		if len(sys.argv) != 4:
			print("\n-- Error --\n")
			print("\tInvalid sintax")
			exit()

		#self.register=sys.arg[4]
		self.port_other_Node=sys.argv[3]	
		self.ip_other_Node=sys.argv[2]
		self.loc=sys.argv[1]

		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind("tcp://*:"+PORT_SERVERS)
		print ("Proxy is now listening servers in port "+PORT_SERVERS)
		self.listening()

	def connectToNode(self):
		contextP = zmq.Context()
		socketP = contextP.socket(zmq.REQ)
		#a = input()
		node = "tcp://" + self.ip_other_Node + ":" + self.port_other_Node
		socketN.connect(node)
		#   socketN.send_multipart([b"server",self.IP_SERVER.encode(),self.PORT_SERVER.encode(),str(self.f_space).encode()])
		"""req = socketP.recv()
		if req.decode()=="NEXT":
			socketP.send_json(self.register)
		"""
		response = socketN.recv()
		if response.decode()=="OK":
			print ("\nNodo is connected ")
		else:
			print("Error!")