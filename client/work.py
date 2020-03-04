#!/usr/bin/python 

def login(tls_sock):
  print("Send login and password to server.") 
  user_input  = input('-->')
  tls_sock.sendall(user_input.encode())
  print(tls_sock.recv(1024).decode())
  
