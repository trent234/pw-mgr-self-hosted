#!/usr/bin/python 

import sys
import socket
import ssl
import time 

hostname = 'tsz.us'
port = 11030
message = 'Hello, server'

context = ssl.create_default_context()

# create normal socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# wrap the socket and ret an SSL socket that is tied to the context (settings & certs)
connstream = context.wrap_socket(sock, server_hostname=hostname)
print(connstream.version())

# attempt to connect to the server
while True:
    try:
        connstream.connect((hostname, port))
        break;
    except ConnectionRefusedError as error: 
        print(error, ' Trying again...')
        time.sleep(2)

# create ssl connection and do the work
# ssock.connect((hostname, port))
connstream.sendall(message.encode())
data = connstream.recv(1024)
print('Received: ', data)

connstream.shutdown(socket.SHUT_RDWR)
connstream.close()

