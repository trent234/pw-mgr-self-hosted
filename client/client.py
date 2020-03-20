#!/usr/bin/python 

# std libs
import sys
import socket
import ssl
import argparse

def conn_cleanup(tls_sock):
  tls_sock.shutdown(socket.SHUT_RDWR)
  tls_sock.close()

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
  
  # *** client interaction #1: attempt to connect to the server. 
  # *** server interaction #1: server will respond with spam check 
  # response: first char 0 = fail. 1 = success. followed by logs
  try:
    tls_sock.connect((args.hostname, args.port))
    print('[INFO]: ' + tls_sock.version())
  except ConnectionRefusedError as error: 
    print('[ERROR]: ' + str(error))
    exit(1)
  
  # *** client interaction #2: attempt to log in 
  tls_sock.sendall((args.username + ' ' + args.password).encode())
  server_response = tls_sock.recv(1024).decode()
  success = int(server_response[0])
  server_response = server_response[1:]
  # *** server interaction #3: 0 means we failed login either bc of spam or bad login info. server conn closed.
  if success == 0:
    conn_cleanup(tls_sock)
    print(str(server_response))
    exit(1)

  # client interaction #3: attempt to complete user's request 
  if args.action.upper() == 'CREATE' or args.action.upper() == 'UPDATE':
    if len(args.account) != 2:
      print('[FAIL]: Two args needed for --account if --action == create or update. [newacct newpw] two strings were not detected.')
      conn_cleanup(tls_sock)
      exit(1)
    tls_sock.sendall((args.action + ' ' + args.account[0] + ' ' + args.account[1]).encode())
  elif args.action.upper() == 'READ' or args.action.upper() == 'DELETE':
    tls_sock.sendall((args.action + ' ' + args.account[0]).encode())
  else:
    print('[FAIL]: No valid action given. CREATE/READ/UPDATE/DELETE are you options.') 
    conn_cleanup(tls_sock)
    exit(1)
    
  server_response = tls_sock.recv(1024).decode()
  divider = server_response.find(' ',0,len(server_response))
  success = server_response[0:divider]
  server_response = server_response[divider + 1:]

  # *** server interaction #3: start with either fail/succes code or pw depending on request followed by logs. 
  # see server comment for more info.
  print(server_response)
  print(success)
  
  conn_cleanup(tls_sock)

if __name__ == '__main__':
  main()
