#!/usr/bin/env python3

# Importing libraries
import socket
import sys
import hashlib

h = hashlib.sha1()
chunk = 0

# Lets catch the 1st argument as server ip
if (len(sys.argv) > 1):
    ServerIp = sys.argv[1]
else:
    print("\n\n Run like \n python3 client.py < serverip address > \n\n")
    exit(1)


# Now we can create socket object
s = socket.socket()

# Lets choose one port and connect to that port
PORT = 9898

# Lets connect to that port where server may be running
s.connect((ServerIp, PORT))

#Open one recv.txt file in write mode
#file = open("./ArchivosCliente/recv.txt", "wb")
#print("\n Copied file name will be recv.txt at server side\n")

# Send data
message = 'Listo'
print("\n " + message)
s.send(message.encode())

# Look for the response
conexiones = s.recv(4).decode()
print("\n\n Conexiones: " + conexiones)

s.send("OK".encode())

client = s.recv(4).decode()
print("\n\n Id Thread: "+client)
file = open(f"./ArchivosRecibidos/Cliente{client}-Prueba-{conexiones}.txt", "wb") 

s.send("OK".encode())

hash_server = s.recv(40).decode()
print("\n\n Hash server: " + hash_server)

s.send("OK".encode())

# Receive any data from client side
RecvData = s.recv(1024)
while RecvData:
    h.update(RecvData)
    file.write(RecvData)
    RecvData = s.recv(1024)

hash_f = h.hexdigest()
print("\n\n Hash file: " + hash_f)

if hash_f == hash_server:
    print("\n\n No se modifico el documento.")
else:
    print("\n\n ERROR: se modifico el documento")

# Close the file opened at server side once copy is completed
file.close()
print("\n\n File has been copied successfully \n")

# Close the connection from client side
s.close()
