import sys
import zmq
import json
import os

sizePart = 1024*1024*10  #bytes
PORT_SERVERS = "8002"
register_server={}
"""
{ip+":"+port:espacio}}
"""
main_register={}
"""
{
	sha256.decode():
		{
		"parts":[] 	#partes del archivo
		"loc":[]	#ip donde esta cada una
		}
}
"""
class Proxy:
	def Start(self):
		os.system("clear")
		print("\n-- Welcome to UltraServer¢2019 --\n")
		print(".SYNTAX: python3 proxy.py <register> \n")
		print(".\tTo initialize the proxy provide a file to register the servers")
		print(".\t<register>\t register of contained files (will be create if doesn't exist)\n")
		print(".\tThis file must be in the same folder of this file an you should called like an argument")
		print(".\tExample: python3 proxy.py servers.json\n")

		self.reg_file=sys.argv[1]	

		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind("tcp://*:"+PORT_SERVERS)
		print ("\tProxy is now listening servers in port "+PORT_SERVERS)
		self.listening()
	
	def listening(self):
		while True:
			parts=[]
			print("\nListening ...\n")
			who,*rest = self.socket.recv_multipart()
			if who.decode()=="server":
				print("Welcome server: ")
				ip,port,parts = rest
				print(ip.decode(),port.decode(),parts.decode())
				"""
				self.socket.send(b"NEXT") 
				json_server = self.socket.recv_json()
				#register_server=json.load(json_server)
				#print(json_server)
				"""
				#register_server.update({[ip,port]:[hash_file,hash_parts]})

				self.socket.send(b"OK")

			elif who.decode()=="client":
				print("Welcome client: ")
				operation=rest[0]
				self.socket.send(b"OK")
				if operation.decode()=="upload":
					print("vamos a ver")
					parts=self.socket.recv_json()
					#self.socket.send(b"OK")
					loc=["192.168.8.16:8000","192.168.8.16:8000","192.168.8.16:8000","192.168.8.16:8000","192.168.8.16:8000","192.168.8.16:8000"]
					loc2=[x.encode() for x in loc]
					self.socket.send_multipart(loc2)
					print(parts)
				#elif operation.decode()=="download":
				#	for in range

			print("Operation complete successfully!")

if __name__ == '__main__':
	Proxy = Proxy()
	Proxy.Start()
