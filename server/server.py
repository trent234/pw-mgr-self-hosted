#!/usr/bin/python 

import socket
import ssl
import time 

hostname = 'tsz.us'
port = 1030

# set context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/etc/letsencrypt/live/tsz.us/fullchain.pem', '/etc/letsencrypt/live/tsz.us/privkey.pem')

# create a new socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind(('tsz.us', port))
sock.listen(1)

# now deal with incoming connections from clients
while True:
    # get the new socket from client side
    newsocket, fromaddr = bindsocket.accept()
    with open('log', 'a') as log:
        print('[', time.localtime(), '] ', fromaddr, ': Connected')
    # create server-side SSL socket for the connection 
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
        deal_with_client(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
    with open('log', 'a') as log:
        print('[', time.localtime(), '] ', fromaddr, ': Disconnected')

def deal_with_client(connstream):
    data = connstream.recv(1024)
    # empty data means the client is finished with us
    while data:
        with open('log', 'a') as log:
            print('[', time.localtime(), '] ', fromaddr, ': ', data)
        connstream.sendall(b'Message logged')
        data = connstream.recv(1024)
