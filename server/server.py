#!/usr/bin/python 

import socket
import ssl
import time 
from datetime import datetime

# this is the actual server side program that best thing to do is probably move to seperate file
def deal_with_client(connstream):
    data = connstream.recv(1024)
    # empty data means the client is finished with us
    while data:
        with open('log', 'a') as log:
            now = datetime.now()
            print('[', now.strftime("%m/%d/%Y, %H:%M:%S"), '] ', fromaddr, ': ', data, file=log)
        connstream.sendall(b'Message logged')
        data = connstream.recv(1024)

# hostname = 'tsz.us'
hostname = '192.168.1.100'
port = 11030

# set context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/etc/letsencrypt/live/tsz.us/fullchain.pem', '/etc/letsencrypt/live/tsz.us/privkey.pem')

# create a new socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind((hostname, port))
sock.listen(2)

# now deal with incoming connections from clients
while True:
    # get the new socket from client side
    newsocket, fromaddr = sock.accept()
    with open('log', 'a') as log:
        now = datetime.now()
        print('[', now.strftime("%m/%d/%Y, %H:%M:%S"), '] ', fromaddr, ': Connected', file=log)
    # create server-side SSL socket for the connection 
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
        deal_with_client(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
    with open('log', 'a') as log:
        now = datetime.now()
        print('[', now.strftime("%m/%d/%Y, %H:%M:%S"), '] ', fromaddr, ': Disconnected', file=log)

