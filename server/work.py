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
  return credentials[0] if sql_cursor.rowcount == 1 else None

def log_ip(sql_cursor, client_ip, success):
  sql_cursor.execute("INSERT INTO client_ip_log VALUES (\'" + str(client_ip) + "\', \'" \
    + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\', " + str(success) + ")")
  
def ip_spam_check(sql_cursor, client_ip):
  max_time = datetime.now() - timedelta(seconds=300)
  sql_cursor.execute("SELECT COUNT(ip) from client_ip_log WHERE ip=\'" + str(client_ip) \
    + "\' AND success=False AND date > \'" + max_time.strftime('%Y-%m-%d %H:%M:%S') + "\'")
  fail_count = sql_cursor.fetchone()[0]
  return fail_count
