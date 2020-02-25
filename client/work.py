#!/usr/bin/python 

# the actual communication between client/server once the connection is setup
def actual_program(connstream):
  while True:
    print("Send message to server. Send \"end\" to terminate the session.")
    user_input  = input('-->')
    connstream.sendall(user_input.encode())
    data = connstream.recv(1024)
    print('Received: ', data.decode())
    if user_input == 'end': 
      print("Empty string detected. Exiting.")
      break
    if data.decode() == '': 
      print("Connection lost from server. Exiting.")
      break
