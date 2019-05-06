import socket
import select
from threading import Thread
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 2:
	print("Incorrect usage: script, port number")
	exit()
IP_address = '127.0.0.1'
Port = int(sys.argv[1])
server.bind((IP_address, Port)) 
server.listen(100)
list_of_clients=[]

def clientthread(conn, user):

	while True:
		try: 
			message = conn.recv(2048).decode() 
			if message:
				print (user[0] + ": " + message)
				message_to_send = user[0] + ": " + message
				broadcast(message_to_send,conn)
			else:
				print(user[0]+': has disconnected')
				remove(conn)
				break
		except:
			print("Thread Ended")
			remove(conn)
			break

def broadcast(message,connection):
	for clients in list_of_clients:
		if clients[2]!=connection:
			try:
				clients[2].sendall(message.encode())
			except:
				clients[2].close()
				remove(clients[2])

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)
		connection.close()

while True:
	conn, addr = server.accept()
	print("Connection Accepted")
	uname= conn.recv(2048)
	user= (uname.decode(), addr, conn)
	list_of_clients.append(user)
	print(uname.decode() + " connected")
	thread=Thread(target=clientthread,args=(conn,user))
	thread.start()


conn.close()
server.close()
