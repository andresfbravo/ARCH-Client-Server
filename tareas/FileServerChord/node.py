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
		print("SYNTAX: python3 node.py ip_Other_Node \n")
		print("\tTo initialize Chord provide ")
		print("\tThis file must be in the same folder of this file an you should called like an argument")
		

		self.register = {}
		
		if len(sys.argv) != 5:
			print("\n-- Error --\n")
			print("\tInvalid sintax")
			exit()

		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind("tcp://*:"+PORT_SERVERS)
		print ("Proxy is now listening servers in port "+PORT_SERVERS)
		self.listening()

		
