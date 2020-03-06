# password manager


protocol:
client send string with user / pass with space between
server will respond with first byte 0 or 1 for success
and every subsequent byte is logs

then part 2 to still finish is client sends [action account pw] for create / update
or [action account] for read delete
client will respond with 0 or 1 again for success followed by logs
and then final line will be the password or it or... None for a delete

To do:

fido2 for 2fa
RFC writeup

Done:

pw mgr:
actual db for "password" key val pairs
server and client programs connect
login feature checks client input agains login db
login spam / brute force check checks for repeated failed logins

server setup:
pi with raspian
router port forwards
ddns for domain use
ssh access / this program access
certs for tls


