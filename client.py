import socket      
import numpy
import mlsocket

s = mlsocket.MLSocket()           
host = socket.gethostname()   
port = 60000                    

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
