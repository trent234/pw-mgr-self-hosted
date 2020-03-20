# password manager

## protocol:
* 1)
* tls handshaking / init connection
* server will respond with first byte 0 or 1 for success of login spam check followed by logs
* 2)
* client send string with user / pass with space between
* server will respond with first byte 0 or 1 for success of login credentials followed by logs
* 3)
* client sends [action account pw] for create / update
* or [action account] for read delete
* server will respond on success with pw (or 1 for delete action) followed by logs
* fail = 0 followed by logs

## To do:

* fido2 for 2fa
* sql injection prevention

## Done:

* RFC writeup

### pw mgr:
* server and client programs connect via tls/ssl
* serverside mariadb server setup / init / db and tables constructed
* login spam / brute force check checks for repeated failed logins
* login feature checks client input agains login db
* actual db for "password" key val pairs
* create/read/update/delete functionality bundle
* formatted response from server in part to match the spec listed above

### server setup:
* pi with raspian linux
* router forwards port used for the program (and others required for setup: http(s) & ssh)
* acquire a domain from a domain registrar
* setup DDNS to point DDNS provider subdomain to my public facing IP
* setup ddclient on the server to check for new public facing IP from ISP so that it updates the DDNS entry accordingly so DDNS always points to the correct IP
* set up CNAME record pointing my domain to my DDNS subdomain
* setup letsencrypt/certbot to generate tls/ssl certificated on the server to allow tls connections


