#!/usr/bin/python3 

# std lib
import time
from datetime import datetime
from datetime import timedelta

def client_login(sql_cursor, username, password):
  sql_cursor.execute("SELECT * FROM logins WHERE username = \"" + username \
    + "\" AND password = \"" + password + "\"")
  sql_cursor.fetchone()
  return username if sql_cursor.rowcount == 1 else False 

def log_ip(sql_cursor, client_ip, success):
  sql_cursor.execute("INSERT INTO client_ip_log VALUES (\'" + str(client_ip) + "\', \'" \
    + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\', " + str(success) + ")")
  
def ip_spam_check(sql_cursor, client_ip):
  max_time = datetime.now() - timedelta(seconds=300)
  sql_cursor.execute("SELECT COUNT(ip) from client_ip_log WHERE ip=\'" + str(client_ip) \
    + "\' AND success=False AND date > \'" + max_time.strftime('%Y-%m-%d %H:%M:%S') + "\'")
  return sql_cursor.fetchone()[0]

# request[0] = action request[1] = new account request[2] = new pw
def create(sql_cursor, username, request):
  # fail if the username / account combo already exist
  sql_cursor.execute("SELECT * FROM pw WHERE username = \'" + username + "\' AND account = \'" + request[1] + "\'")
  sql_cursor.fetchone()
  if sql_cursor.rowcount >= 1: 
    return False
  sql_cursor.execute("INSERT INTO pw VALUES (\'" + username + "\', \'" + request[1] + "\', \'" + request[2] + "\')") 
  return True 
  
# request[0] = action request[1] = new account request[2] = new pw
def update(sql_cursor, username, request):
  sql_cursor.execute("SELECT * FROM pw WHERE username = \'" + username + "\' AND account = \'" + request[1] + "\'")
  sql_cursor.fetchone()
  if sql_cursor.rowcount != 1:
    return False
  sql_cursor.execute("UPDATE pw SET password = \'" + request[2] + "\' where username=\'" + username + "\' AND account = \'" + request[2] + "\'") 
  return True 

# request[0] = action request[1] = new account request[2] = new pw
def read(sql_cursor, username, request):
  sql_cursor.execute("SELECT * FROM pw WHERE username = \'" + username + "\' AND account = \'" + request[1] + "\'")
  record = sql_cursor.fetchone()
  if sql_cursor.rowcount != 1:
    return 0 
  # [0]username [1]acct [2]password
  return record[2] 

# request[0] = action request[1] = new account request[2] = new pw
def delete(sql_cursor, username, request):
  sql_cursor.execute("DELETE FROM pw WHERE username = \'" + username + "\' AND account = \'" + request[1] + "\'")
  if sql_cursor.rowcount != 1:
    return False
  return True
