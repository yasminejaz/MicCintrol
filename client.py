import socket      # Import socket module
import numpy
import mlsocket

s = mlsocket.MLSocket()           # Create a socket object
host = socket.gethostname()   # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
s.send(str.encode("Hello server!"))

with open('received_file.txt', 'a') as f:
    print('file opened')
    while True:
        print('receiving data...')

        numpy.savetxt(f,s.recv(1024))

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
