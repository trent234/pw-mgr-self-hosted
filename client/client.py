#!/usr/bin/python 

# std libs
import sys
import socket
import ssl
import argparse

def main():
  parser = argparse.ArgumentParser(description='Retrieve a password securely.')
  parser.add_argument('--hostname', required=True, \
    help='the hostname to connect to')
  parser.add_argument('--port', required=True, type=int, \
    help='the port on the server to connect to')
  parser.add_argument('--username', required=True, \
    help='the username you wish to login as')
  parser.add_argument('--password', required=True, \
    help='the password for the username. if omitted, you will be prompted to write your password')
  parser.add_argument('--account', required=True, \
    help='the account whose password you are concerned with')
  parser.add_argument('--action', required=True, \
    help='argument options: create, read, update, delete')
  parser.add_argument('--verbose', required=False, action='store_true', \
    help='no args. if written, messages will be included about the operation of the program')
  args = parser.parse_args()

  # create normal socket
  tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
  # wrap the socket and ret an TLS/SSL socket that is tied to the context (settings & certs)
  context = ssl.create_default_context()
  tls_sock = context.wrap_socket(tcp_sock, server_hostname=args.hostname)
  
  # attempt to connect to the server
  try:
    tls_sock.connect((args.hostname, args.port))
    print('[INFO]: ' + tls_sock.version())
  except ConnectionRefusedError as error: 
    print('[ERROR]: ' + error)
    exit(1)
  
  # attempt to log in
  tls_sock.sendall((args.username + ' ' + args.password).encode())
  print(tls_sock.recv(1024).decode())

  # attempt to complete user's request 
  tls_sock.sendall((args.account + ' ' + args.action).encode())
  print(tls_sock.recv(1024).decode())
  
  tls_sock.shutdown(socket.SHUT_RDWR)
  tls_sock.close()

if __name__ == '__main__':
  main()
