import numpy
import mlsocket

port = 60000                    # Reserve a port for your service.
s = mlsocket.MLSocket()             # Create a socket object
host = ''                           # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print('Server listening....')

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    data = conn.recv(1024)
    print('Server received', repr(data))

    with open('received_file.txt', 'a') as f:
        print('file opened')
        while conn:
            print('receiving data...')

            numpy.savetxt(f, conn.recv(1024))

    f.close()
    print('Successfully get the file')
    s.close()
    print('connection closed')
    break

