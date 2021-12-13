# RATTTY
***
Required packages:
1. Scapy

## Description
RAATTTY is desgined to allow the sending and receiving of commonds between remote hosts. The package consists of a server
and an agent. 
***
## Usage
There are some considerations to make before deploying the TCPClient agent, which port will the agent listen on. 
Once the port has been decided set the local port(self.LPORT) in TCPClient to the desired port. Start the TCPServer and TCPClient
in TCPServer enter ping in the prompt. Ping sends a TCP packet to the agent on the set listening port. This triggerns the
agent to initiate a connection with the server. 

### Server Commands
kill: Ends the connection and returns user to the main prompt
keylogger(deprecated): Starts the keylogger
***
