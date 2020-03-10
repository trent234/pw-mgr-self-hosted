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
  parser.add_argument('--account', required=True, nargs='+', \
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
    print('[ERROR]: ' + str(error))
    exit(1)
  
  # *** client query #1: attempt to log in ***
  tls_sock.sendall((args.username + ' ' + args.password).encode())
  login_response = tls_sock.recv(1024).decode()
  success = login_response[0]
  login_response = login_response[1:]
  print(login_response)
  if success == 0:
    exit(1)

  # attempt to complete user's request 
  if args.action.upper() == 'CREATE' or args.action.upper() == 'UPDATE':
    if len(args.account) != 2:
      print('[FAIL]: Two args needed for --account if --action == create or update. [newacct newpw] two strings were not detected.')
      exit(1)
    tls_sock.sendall((args.action + ' ' + args.account[0] + ' ' + args.account[1]).encode())
    print(tls_sock.recv(1024).decode())
  
  tls_sock.shutdown(socket.SHUT_RDWR)
  tls_sock.close()

if __name__ == '__main__':
  main()
