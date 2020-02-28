#!/usr/bin/python 

# stl
import sys
import socket
import mariadb
import ssl
import time 
from datetime import datetime
# user defined
import work

#location needs to be the directory + filename of a text file with 4 lines containing:
# username, password, ip(likely localhost), and port(default 3306 is a keeper)
def db_connect(location):
  try:
    login_info = open(location, "r").readlines()
  except FileNotFoundError as e:
    print(f"Error opening file for db credentials: {e}")
    sys.exit(1)
    
  try:
    conn = mariadb.connect(
    user=login_info[0].rstrip(),
    password=login_info[1].rstrip(),
    host=login_info[2].rstrip(),
    port=int(login_info[3].rstrip()))
  except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
     
  return conn

def conn_cleanup(tls_sock, sql_conn, client_addr):
# clean up on the way out
  sql_conn.close()
  tls_sock.shutdown(socket.SHUT_RDWR)
  tls_sock.close()
  with open('log', 'a') as log:
    now = datetime.now()
    print('[', now.strftime("%m/%d/%Y, %H:%M:%S"), '] ', client_addr, ': Disconnected', file=log)


def usage():
  print('usage: ./client.py hostname lan_static_ip port')
  exit(0)

def main():
  if len(sys.argv) < 3:
    usage()
 
  lan_static_ip = sys.argv[2] # 192.168.1.100 
  port = int(sys.argv[3]) # 11030
  cert_dir = ('/etc/letsencrypt/live/' + sys.argv[1] + '/')


  # set tls context
  context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
  context.load_cert_chain(cert_dir + 'fullchain.pem', cert_dir + 'privkey.pem')
  
  # create a regular tcp new socket (gets wrapped in tls once tcp connected.. is this not ideal?)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
  sock.bind((lan_static_ip, port))
  sock.listen(2)
  
  # now deal with incoming connections from clients
  while True:
    # sit, wait until client tries to connect to the port for this program 
    tcp_sock, client_addr = sock.accept()
    with open('log', 'a') as log:
      now = datetime.now()
      print('[', now.strftime("%m/%d/%Y, %H:%M:%S"), '] ', client_addr, ': Connected', file=log)
    # create server-side SSL socket for the connection 
    tls_sock = context.wrap_socket(tcp_sock, server_side=True)
    # connect to sql db and then, for interacting with db, use a cursor obj
    sql_conn = db_connect('sql_login')
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute("USE pw_mgr_db")
    # username/pw login check phase
    user = work.client_login(tls_sock, sql_cursor) 
    if user == None:
      tls_sock.sendall(b'Login credentials invalid. Exiting.')
      conn_cleanup(tls_sock, sql_conn, client_addr)
    else:
      tls_sock.sendall(b'You\'ve successfully logged in ' + user.encode() + b'!')
      # here we do the retrieval of the password for the account and all the other jazz thats the point of this program
      conn_cleanup(tls_sock, sql_conn, client_addr)

if __name__ == '__main__':
  main()
