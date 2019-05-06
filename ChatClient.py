import socket
import select
import sys
import os
import errno
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 2:
	print("InCorrect usage: script, port number")
	exit()
IP_address = '127.0.0.1'
Port = int(sys.argv[1])
print("What is your username? : ")
def connection(IP, Port):
		
	try:	
		server.connect((IP, Port))
		#print("Connected")
	except:
		time.sleep(3)
		connection(IP,Port)
		print("Retry")
connection(IP_address, Port)
uname=sys.stdin.readline().strip()
u=uname.encode()

server.send(u)
		
while True:
	sockets_list = [sys.stdin, server]
	read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048).decode()
			print(message)
		else:
			try:
				message = input()
				server.send(message.encode())
				sys.stdout.flush()
			except EOFError:
				os._exit(0)
server.close()
