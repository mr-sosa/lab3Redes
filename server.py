#!/usr/bin/env python3

# Importing socket library 
import socket
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

# Now we can create socket object
s = socket.socket()

# Lets choose one port and start listening on that port
PORT = 9898
print("\n Server is listing on port :", PORT, "\n")

# Now we need to bind to the above port at server side
s.bind(('', PORT))

# Now we will put server into listenig  mode 
s.listen(10)

#Variable hash
hash_value = ""

# Seleccion
print("Seleccione el archivo que quiere enviar:")
print("1. Archivo 100MB")
print("2. Archivo 250MB")
print("3. Archivo prueba")
archivo = input()
if archivo=="1":
    file = open("./ArchivosServidor/file100MB.txt", "rb") 
    hash_value = hash_file("./ArchivosServidor/file100MB.txt")
elif archivo == "2":
    file = open("./ArchivosServidor/file250MB.txt", "rb") 
    hash_value = hash_file("./ArchivosServidor/file250MB.txt")
elif archivo == "3":
    file = open("./ArchivosServidor/sample1.txt", "rb")
    hash_value = hash_file("./ArchivosServidor/sample1.txt") 

clients = input("Número de clientes a los cuales desea enviar el archivo: ")

SendData = file.read(1024)


# Now we do not know when client will concatct server so server should be listening contineously  
while True:
    # Now we can establish connection with clien
    conn, addr = s.accept()
    
    estado = conn.recv(1024).decode()

    print("\n\n Estado del cliente: " + estado + "\n\n")

    if estado == 'Listo':
        conn.send(str(clients).encode())
        print(str(hash_value))
        conn.send(str(hash_value).encode())

        while SendData:
            #Now send the content of sample.txt to server
            conn.send(SendData)
            SendData = file.read(1024)
        
    
      

    # Close connection with client
    conn.close()
    print("\n Server closed the connection \n")

    # Come out from the infinite while loop as the file has been copied from client.
    break
