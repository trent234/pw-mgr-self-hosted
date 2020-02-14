# password manager
Password manager

Passwords are managed and stored in an encrypted state on a server. 
Client sends password over a TLS connection
### Server 
 - Needs to have a static ip (public facing IP or server's IP behind router on LAN?)
 	** I believe public IP will have to be variably assigned just because thats the nature of Comcast & personal accounts. But thats OK, our DDNS will sort it out for us.
 - Have dynamic dns set up server side. public facing.
 	Set up on router, but if its not an option we have ddclient package to work with
 	https://wiki.archlinux.org/index.php/Dynamic_DNS
 - Assign static ip to server on its gateway protected local network. 
 - But the gateway could reset and receive a new public facing Ip
    - Need a DNS service to update this new ip if it changes.
    - Need to provide a way to update gateways local dns record with the local server Id. (Linux util, or programitically in higher level language. 
 - Server program is tsl socket networking based, there are a few functions: normal user can create/remove/update/delete key value pairs that are websites and passwords. Can only access those records associated with user's username.
  	All connection data gets logged into database as well e.g IP login time, login attempts, etc
 	admin user can log in and get summary of usage by date, frequency, etc
 	using connection data, prevent repeated faild logins and other abuses by IP, time, or other metrics.
### Client
needs to open TLS connection with the server. 
  - Send username and master password. 
  - If the username doesn’t exist then create one.  
  - Enter the password they want to add, and the key associated with it (what it’s for)
  - Retrieve passwords by key

### Things we need to figure out:
How to initiate a direct secure connection between the client and the server. Should we use TLS? Is there another one more suitable for sending a small variety of short commands?

I think tsl is pretty program agnostic. i'm seeing that its the protocol that lets http be https. so i'm thinking the connection will be pretty application agnostic.. like how tcp doesn't care what the application layer uses it for. also, i found this library... it may be exaclty the kind of thing we're not allowed to use but is interesting.
https://en.wikipedia.org/wiki/OpenSSL

TLS involves getting TLS certifications, can maybe involve a free service or software/library into our code that generates these certifications. 
https://letsencrypt.org/

How to make sure DNS is properly configured to ensure we can easily find our server from behind any network. 
I think DDNS will take care of this. if the DNS tables are updated, all clients will be able to find it when their DNS query returns the updated server IP.

How to program the socket interfaces on the client and the server. 
When I was looking for how tsl/ssl socket network programming differs from the norm, stack overflow ppl mention OpenSSL as the "standard for C developers". Still not be what we want and to much of a library cheat but worth noting.
https://stackoverflow.com/questions/7698488/turn-a-simple-socket-into-an-ssl-socket

python looks to be the same. from the docs:
https://docs.python.org/3/library/ssl.html
Actually nvm this is baked right into the standard python3 libs. this should be not much harder than normal tcp sockets once we understand the handshaking and certificate checking stuff. 

How to ensure the important information is properly encrypted and secured, even if packets are sniffed. 
Ensure? Good question.. penetration testing? Something like this may be a good confirmation-
https://doxsec.wordpress.com/2017/04/23/tls-ssl-penetration-testing/
Also using WireShark to see if we can see anything may be a good test.

A secure method to encrypt the database of the server. Stored in SQL tables. 
Very interesting info here. Only read about half of it, but it provides hashing libs for
some languages.
https://www.codeproject.com/Articles/704865/Salted-Password-Hashing-Doing-it-Right

FIDO2/WC3/CTAP
adding a hardware 2FA could be a goal as well
https://en.wikipedia.org/wiki/FIDO2_Project
https://www.w3.org/TR/2019/REC-webauthn-1-20190304/#intro
