#!/usr/bin/python 

# std libs
import sys
import socket
import ssl
import time 
# user defined libs
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
  tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
  # wrap the socket and ret an TLS/SSL socket that is tied to the context (settings & certs)
  tls_sock = context.wrap_socket(tcp_sock, server_hostname=hostname)
  print(tls_sock.version())
  
  # attempt to connect to the server
  while True:
    try:
      tls_sock.connect((hostname, port))
      break;
    except ConnectionRefusedError as error: 
      print(error, ' Try again? (y/n)')
      response = input()
      if (response != 'y'):
        print('Goodbye.')
        sys.exit()
  
  work.login(tls_sock)  
  
  tls_sock.shutdown(socket.SHUT_RDWR)
  tls_sock.close()

if __name__ == '__main__':
  main()
