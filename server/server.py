#!/usr/bin/python3 

# std libs
import sys
import socket
import mariadb
import ssl
import time 
from datetime import datetime
import argparse
# user defined
import work

# clean up on the way out
def conn_cleanup(tls_sock, sql_conn, client_addr):
  sql_conn.close()
  tls_sock.shutdown(socket.SHUT_RDWR)
  tls_sock.close()

#location needs to be the directory + filename of a text file with 4 lines containing:
# username, password, ip(likely localhost), and port(default 3306 is a keeper)
def db_connect(location):
  try:
    login_info = open(location, "r").readlines()
  except FileNotFoundError as error:
    print("[SERVER]: Error opening file for db credentials: " + error + " at location " + location)
    sys.exit(1)
    
  try:
    conn = mariadb.connect(
    user=login_info[0].rstrip(),
    password=login_info[1].rstrip(),
    host=login_info[2].rstrip(),
    port=int(login_info[3].rstrip()))
  except mariadb.Error as error:
    print("[SERVER]: Error connecting to MariaDB Platform: " + error)
    sys.exit(1)
     
  return conn

def main():
  parser = argparse.ArgumentParser(description='Server host for password retrieval program.')
  parser.add_argument('--hostname', required=True, help='our hostname')
  parser.add_argument('--port', required=True, type=int, help='the port on the server')
  parser.add_argument('--lan_ip', required=True, help='the server\'s static ip in the lan')
  args = parser.parse_args()

  cert_dir = ('/etc/letsencrypt/live/' + args.hostname + '/')

  # set ssl/tls context
  context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
  context.load_cert_chain(cert_dir + 'fullchain.pem', cert_dir + 'privkey.pem')
  
  # create a regular tcp new socket 
  tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
  # create server-side TLS/SSL socket for the connection by wrapping a tcp socket
  tls_sock = context.wrap_socket(tcp_sock, server_side=True)
  tls_sock.bind((args.lan_ip, args.port))
  tls_sock.listen(1)
  
  # now deal with incoming connections from clients
  while True:
    # *** client interaction #1: initiates connection
    # wait until client tries to connect to the port for this program. then make connection.
    # and fire up sql db and then, for interacting with db, use a cursor obj
    tls_conn, client_addr = tls_sock.accept()
    sql_conn = db_connect('sql_login')
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute("USE pw_mgr_db")
    log = ''
    pw = 0

    # *** server interaction #1: resp to a connection attempt. 0 = fail 1 = success. subsequent strings = log 
    # Guard against spam attempts to log in / brute force      
    attempt_count = work.ip_spam_check(sql_cursor, client_addr[0]) 
    if attempt_count > 4:
      work.log_ip(sql_cursor, client_addr[0], 'False')
      log += ('[FAIL]: ' + str(attempt_count) + ' spam attempts detected from this IP.\n ')
      tls_conn.sendall(str(pw).encode() + log.encode())
      conn_cleanup(tls_conn, sql_conn, client_addr)
      continue

    # *** client interaction #2: username/pw login check phase. log ip either way for records.
    # *** server interaction #2: resp to a login attempt. 0 = fail 1 = success. subsequent strings = log 
    credentials = tls_conn.recv(1024).decode().split()
    if len(credentials) != 2:
      log += (b'[FAIL]: Syntax is [username password]. Two seperate strings not detected here.')
      tls_conn.sendall(str(pw).encode() + log.encode())
      conn_cleanup(tls_conn, sql_conn, client_addr)
      continue
    user = work.client_login(sql_cursor, credentials[0], credentials[1]) 
    if user == False:
      work.log_ip(sql_cursor, client_addr[0], 'False')
      log += ('[FAIL]: Login credentials invalid.\n ')
      tls_conn.sendall(str(pw).encode() + log.encode())
      conn_cleanup(tls_conn, sql_conn, client_addr)
      continue
    work.log_ip(sql_cursor, client_addr[0], 'True')
    log += ('[INFO]: Login for user \"' + user + '\" is successful.\n ')
    pw = 1
    tls_conn.sendall(str(pw).encode() + log.encode())
    #reset log after transmit
    log = '' 
    pw = 0
    
    # *** client interaction interaction #3 send either "create/update account pw" 
    # or "read/delete account"
    # *** server interaction #3: attempt to carry out task. create/read/update: pw followed by subsequent strings = log. 
    # delete: 1 followed by subsequent strings = 1og. for all: if fail then 0 followed by log strings.
    request = tls_conn.recv(1024).decode().split()
    if not request:
      conn_cleanup(tls_conn, sql_conn, client_addr)
      continue
    if request[0].upper() == 'CREATE':
      if work.create(sql_cursor, user, request) == False:
        log += ('[FAIL]: that account already exists for this user.')
      else: 
        log += ('[INFO]: new record created.')
        pw = request[2]
    elif request[0].upper() == 'UPDATE':
      if work.update(sql_cursor, user, request) == False:
        log += ('[FAIL]: that account doesn\'t exist for this user.')
      else:
        log += ('[INFO]: record\'s password has been updated.')
        pw = request[2]
    elif request[0].upper() == 'READ':
      pw = work.read(sql_cursor, user, request)
      if pw == 0:
        log += ('[FAIL]: That account doesn\'t exist for your account, so no pw could be retrieved.')
      else:
        log += ('[INFO]: record has been retrieved.')
    elif request[0].upper() == 'DELETE':
      if work.delete(sql_cursor, user, request) == False:
        log += ('[FAIL]: No account with that name, so can\'t delete any pw for it.')
      else:
        pw = 1
        log += ('[INFO]: record has been deleted.')
     
    tls_conn.sendall((str(pw) + ' ' +  log).encode())
      
    conn_cleanup(tls_conn, sql_conn, client_addr)

if __name__ == '__main__':
  main()
