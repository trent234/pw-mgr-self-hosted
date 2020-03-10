# password manager

## protocol:
* tls handshaking / init connection
* client send string with user / pass with space between
* server will respond with first byte 0 or 1 for success
* and every subsequent byte is logs
* if 0, server has terminated the connection 
* two reasons can lead to this- incorrect login, or spamming login attempts from a single ip

* then part 2 to still finish is client sends [action account pw] for create / update
* or [action account] for read delete
* client will respond with 0 or 1 again for success followed the pw followed by logs all space seperated
* delete will have None in pw position

## To do:

* finish adding delete to complete create/read/update/delete functionality bundle
* format response from server in part to to match the spec listed above
* RFC writeup
* fido2 for 2fa
* sql injection prevention

## Done:

### pw mgr:
* server and client programs connect via tls/ssl
* serverside mariadb server setup / init / db and tables constructed
* login spam / brute force check checks for repeated failed logins
* login feature checks client input agains login db
* actual db for "password" key val pairs

### server setup:
* pi with raspian linux
* router forwards port used for the program (and others required for setup: http(s) & ssh)
* acquire a domain from a domain registrar
* setup DDNS to point DDNS provider subdomain to my public facing IP
* setup ddclient on the server to check for new public facing IP from ISP so that it updates the DDNS entry accordingly so DDNS always points to the correct IP
* set up CNAME record pointing my domain to my DDNS subdomain
* setup letsencrypt/certbot to generate tls/ssl certificated on the server to allow tls connections


