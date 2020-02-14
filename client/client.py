#!/usr/bin/python 

import sys
import socket
import ssl
import time 

hostname = 'tsz.us'
port = 1030
message = 'Hello, server'

context = ssl.create_default_context()

# attempt to connect to the server
while True:
    try:
        sock = socket.create_connection((hostname, port), 5)
    except ConnectionRefusedError as error: 
        print(error, ' Trying again...')
        time.sleep(2)

# wrap the socket and ret an SSL socket that is tied to the context (settings & certs)
ssock = context.wrap_socket(sock, server_hostname=hostname)
print(ssock.version())

# create ssl connection and do the work
ssock.connect((hostnane, port))
ssock.sendall(message)
data = ssock.recvall()
print('Received: ', data)
