
# the actual communication between client/server once the connection is setup
def actual_program(connstream):
  user_input  = input('-->')
  connstream.sendall(user_input.encode())
  data = connstream.recv(1024)
  print('Received: ', data)

