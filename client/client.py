#!/usr/bin/python 

# stl
import sys
import socket
import ssl
import time 
# user defined
import work

def usage():
  print('usage: ./client.py hostname port')    
  exit(0)

def main():
  if len(sys.argv) < 2: 
    usage()    

  hostname = sys.argv[1] # tsz.us
  port = int(sys.argv[2]) # 11030
  
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
      print(error, ' Try again? (y/n)')
      response = input()
      if (response != 'y'):
        print('Goodbye.')
        sys.exit()
  
  work.actual_program(connstream)  
  
  connstream.shutdown(socket.SHUT_RDWR)
  connstream.close()

if __name__ == '__main__':
  main()
