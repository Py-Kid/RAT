# RATTTY
***


## Description
RATTTY is designed to allow the sending and receiving of commands between remote hosts. The package consists of a server
and an agent. 
***
## Usage
Set the RHOST and RPORT variables in TCP_Client to the machine that wil be running TCP_Server and run it.
Set the LHOST and LPORT to route-able IP or private ones if being deployed on a LAN and start it. 


### Server Commands
kill: Ends the connection and returns user to the main prompt
help: Shows available commands
list: Shows connect agents
connect: opens a shell with desired agent
***
