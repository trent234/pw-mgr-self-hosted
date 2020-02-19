#!/usr/bin/python 

import sys
import socket
import ssl
import time 
from datetime import datetime

# this is the actual server side program that best thing to do is probably move to seperate file
def actual_program(connstream, fromaddr):
    data = connstream.recv(1024)
    # empty data means the client is finished with us
    while data:
        with open('log', 'a') as log:
            now = datetime.now()
            print('[', now.strftime("%m/%d/%Y, %H:%M:%S"), '] ', fromaddr, ': ', data, file=log)
        connstream.sendall(b'Message logged')
        data = connstream.recv(1024)

def usage():
   print('usage: ./client.py hostname lan_static_ip port')
   exit(0)

def main():
  if len(sys.argv) < 3:
    usage()
 
  lan_static_ip = sys.argv[2] # 192.168.1.100 
  port = int(sys.argv[3]) # 11030
  cert_dir = ('/etc/letsencrypt/live/' + sys.argv[1] + '/')

  # set context
  context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
  context.load_cert_chain(cert_dir + 'fullchain.pem', cert_dir + 'privkey.pem')
  
  # create a new socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
  sock.bind((lan_static_ip, port))
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
          actual_program(connstream, fromaddr)
      finally:
          connstream.shutdown(socket.SHUT_RDWR)
          connstream.close()
      with open('log', 'a') as log:
          now = datetime.now()
          print('[', now.strftime("%m/%d/%Y, %H:%M:%S"), '] ', fromaddr, ': Disconnected', file=log)

if __name__ == '__main__':
  main()
