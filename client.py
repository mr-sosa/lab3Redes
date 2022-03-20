#!/usr/bin/env python3

# Importing libraries
import socket
import sys
import hashlib

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()
   print(h)
   # open file for reading in binary mode
   with open(filename,'rb') as f:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = f.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

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
file = open("./ArchivosCliente/recv.txt", "wb")
print("\n Copied file name will be recv.txt at server side\n")

# Send data
message = 'Listo'
print("\n" + message)
s.send(message.encode())

# Look for the response
client = s.recv(4).decode()
print("\n\n Clients: " + client)
#conexiones = sock.recv(1024).decode()
#print("Co"+conexiones)
#file = open(f"./ArchivosRecibidos/Cliente{client}-Prueba-{conexiones}.txt", "wb") 

hash_server = s.recv(40).decode()
print("\n\n Hash server: " + hash_server)

# Receive any data from client side
RecvData = s.recv(1024)
while RecvData:
    file.write(RecvData)
    RecvData = s.recv(1024)

hash_f = hash_file('./ArchivosServidor/sample1.txt')
print("\n\n Hash file: " + hash_f)

#if hash_f == hash_server:
#    print("No se modifico el documento.")
#else:
#    print("ERROR: se modifico el documento")

# Close the file opened at server side once copy is completed
file.close()
print("\n File has been copied successfully \n")

# Close the connection from client side
s.close()
