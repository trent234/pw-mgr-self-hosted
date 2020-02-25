#!/usr/bin/python 

# stl
import time
from datetime import datetime

# is the actual server side program that best thing to do is probably move to seperate file
def actual_program(connstream, fromaddr):
  data = connstream.recv(1024)
  # empty data means the client is finished with us
  while data:
    with open('log', 'a') as log:
      now = datetime.now()
      print('[', now.strftime("%m/%d/%Y, %H:%M:%S"), '] ', fromaddr, ': ', data, file=log)
    connstream.sendall(b'Message logged')
    data = connstream.recv(1024)

