#!/usr/bin/python 

# std lib
import time
from datetime import datetime
# user def

def client_login(tls_sock, sql_cursor):
  credentials = tls_sock.recv(1024).decode().split()
  sql_cursor.execute("SELECT * FROM logins WHERE username = \"" + credentials[0] + "\" AND password = \"" + credentials[1] + "\"")
  sql_cursor.fetchone()
  return credentials[0] if sql_cursor.rowcount == 1 else None

