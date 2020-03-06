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
    # wait until client tries to connect to the port for this program. then make connection.
    # and fire up sql db and then, for interacting with db, use a cursor obj
    tls_conn, client_addr = tls_sock.accept()
    sql_conn = db_connect('sql_login')
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute("USE pw_mgr_db")

    # Guard against spam attempts to log in / brute force      
    if work.ip_spam_check(sql_cursor, client_addr[0]) > 4:
      attempt_count = work.log_ip(sql_cursor, client_addr[0], 'False')
      tls_conn.sendall(b'[FAIL]: ' + attempt_count + ' spam attempts detected from this IP.')
      conn_cleanup(tls_conn, sql_conn, client_addr)
      continue

    # username/pw login check phase
    user = work.client_login(tls_conn, sql_cursor) 
    if user == None:
      work.log_ip(sql_cursor, client_addr[0], 'False')
      tls_conn.sendall(b'[FAIL]: Login credentials invalid.')
      conn_cleanup(tls_conn, sql_conn, client_addr)
      continue

    # here we do the retrieval of the password for the account 
    # and all the other jazz thats the point of this program
    work.log_ip(sql_cursor, client_addr[0], 'True')
    tls_conn.sendall(b'[INFO]: Login for user: ' + user.encode() + b' is successful.')

    conn_cleanup(tls_conn, sql_conn, client_addr)

if __name__ == '__main__':
  main()
