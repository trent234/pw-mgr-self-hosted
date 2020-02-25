
# the actual communication between client/server once the connection is setup
def actual_program(connstream):
  message = 'Hello, server'
  connstream.sendall(message.encode())
  data = connstream.recv(1024)
  print('Received: ', data)

