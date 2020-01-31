# personal_proj
Who knows! Time to brainstorm.

#1

GPS & microcontroller to generate coordinates!
This is pretty mindblowing that we could do this. It spells it all out, but i bet it would be a challenge nonetheless. If we finish and want to expand on it, we could tackle the power side and use a battery instead of the cable. We could get really into electronics and design a circuit and make a integrated version... and/or figure out another module to link up to cellular connection... at this point we'd have a realtime gps tracker. as far as microcontrollers i like the AVR ones. i have a couple we could use. cheap and the same instruction set as arduino bc thats AVR too.

https://circuitdigest.com/microcontroller-projects/gps-module-interfacing-with-atmega16-32-avr-microcontroller

#2

Anything with cellular connection.. the more i read the more of a pain seems to be. i can't figure out a good route to go. the 2g (edge) boards are nice and simple and cheap but carriers have all but discontinued service for that frequency... basically the same thing is happening for 3g. and then LTE boards are really expensive and overkill. theres some iot frequencies but they are still young: nb-iot and lora... not enough adoption but in a couple years that could be cool idk. this is what niru does for research i think? so maybe we should ask her. but ANYWAY, a backup solution would be to have a proj with a bluetooth module and then write the code (somehow) to link it up to a.. linux phone!? so theres mobility without the lte module as part of the project.

#3

With this we could control a dc motor with code running on our microcontroller. Thats neat and all, but this could be a springboard to even cooler stuff... add a mounted tiny camera to control camera direction (and process video). orr setup a couple motion detectors and sync the motor to turn and record movement?

https://circuitdigest.com/microcontroller-projects/interfacing-dc-motor-with-atmega16-avr-microcontroller

#4

rain sensor... very portlandesque. could have that outside one of our apts.. connected via wifi... give alerts to our phone when its raining at our places. lol

https://circuitdigest.com/microcontroller-projects/rain-detector-using-arduino

i just discovered https://circuitdigest.com/microcontroller-projects/ tonight and it is a treasure trove.


# password manager
Password manager

Passwords are managed and stored in an encrypted state on a server. 
Client sends password over a secure transport
TLS connection
### Server 
 - needs to have a static ip
 - Have dynamic dns set up server side. 
 - Assign static ip to server on its gateway protected local network. 
 - But the gateway could reset and receive a new public facing Ip
    - Need a DNS service to update this new ip if it changes.
    - Need to provide a way to update gateways local dns record with the local server Id. (Linux util, or programitically in higher level language. 
### Client
needs to open TLS connection with the server. 
  - Send username and master password. 
  - If the username doesn’t exist then create one.  
  - Enter the password they want to add, and the key associated with it (what it’s for)
  - Retrieve passwords by key

### Things we need to figure out:
How to initiate a direct secure connection between the client and the server. Should we use TLS? Is there another one more suitable for sending a small variety of short commands?
TLS involves getting TLS certifications, can maybe involve a free service or software/library into our code that generates these certifications. 
How to make sure DNS is properly configured to ensure we can easily find our server from behind any network. 
How to program the socket interfaces on the client and the server. 
How to ensure the important information is properly encrypted and secured, even if packets are sniffed. 
A secure method to encrypt the database of the server. Stored in SQL tables. 
	

