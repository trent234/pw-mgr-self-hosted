#!/usr/bin/python3 

# std lib
import time
from datetime import datetime
from datetime import timedelta

def client_login(tls_conn, sql_cursor):
  credentials = tls_conn.recv(1024).decode().split()
  if len(credentials) != 2:
    tls_conn.sendall(b'[FAIL]: Syntax is [username password]. Two seperate strings not detected here.')
    return None 
  sql_cursor.execute("SELECT * FROM logins WHERE username = \"" + credentials[0] \
    + "\" AND password = \"" + credentials[1] + "\"")
  sql_cursor.fetchone()
  return credentials[0] if sql_cursor.rowcount == 1 else False 

def log_ip(sql_cursor, client_ip, success):
  sql_cursor.execute("INSERT INTO client_ip_log VALUES (\'" + str(client_ip) + "\', \'" \
    + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\', " + str(success) + ")")
  
def ip_spam_check(sql_cursor, client_ip):
  max_time = datetime.now() - timedelta(seconds=300)
  sql_cursor.execute("SELECT COUNT(ip) from client_ip_log WHERE ip=\'" + str(client_ip) \
    + "\' AND success=False AND date > \'" + max_time.strftime('%Y-%m-%d %H:%M:%S') + "\'")
  return sql_cursor.fetchone()[0]

# [0] = action [1] = new account [2] = new pw
def create(sql_cursor, username, request):
  # fail if the username / account combo already exist
  sql_cursor.execute("SELECT * FROM pw WHERE username = \'" + username + "\' AND account = \'" + request[1] + "\'")
  sql_cursor.fetchone()
  if sql_cursor.rowcount >= 1: 
    return False
  sql_cursor.execute("INSERT INTO pw VALUES (\'" + username + "\', \'" + request[1] + "\', \'" + request[2] + "\')") 
  return True 
  
# [0] = action [1] = new account [2] = new pw
def update(sql_cursor, username, request):
  sql_cursor.execute("SELECT * FROM pw WHERE username = \'" + username + "\' AND account = \'" + request[1] + "\'")
  sql_cursor.fetchone()
  if sql_cursor.rowcount != 1:
    return False
  print("UPDATE pw SET password = \'" + request[2] + "\' where username=\'" + username + "\' AND account = \'" + request[2] + "\'") 
  sql_cursor.execute("UPDATE pw SET password = \'" + request[2] + "\' where username=\'" + username + "\' AND account = \'" + request[2] + "\'") 
  return True 

# [0] = action [1] = new account [2] = new pw
def read(sql_cursor, username, request):
  sql_cursor.execute("SELECT * FROM pw WHERE username = \'" + username + "\' AND account = \'" + request[1] + "\'")
  a = sql_cursor.fetchone()
  print("this is it: " + a)
  if sql_cursor.rowcount != 1:
    return False
  return True
