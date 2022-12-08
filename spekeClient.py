import random
import hashlib
import socket
import time

from libnum import invmod

class spekeClient:
    def __init__(self, p, g):
        self.p = p
        self.g = g

    def validate_key(self):
        s = socket.socket()        
        port = 11122               
        s.connect(('127.0.0.1', port))
    
        self.p = int(s.recv(1024).decode())
        time.sleep(1)
        self.g = int(s.recv(1024).decode())
        time.sleep(1)
    
        a = int(s.recv(1024).decode())
        time.sleep(1)
        print("    => Received from server...")

        b = random.randint(0, self.p-1)
        client_to_send = pow(self.g, b, self.p)
        s.send(str(client_to_send).encode())
        print("    => Sent to server...")
        time.sleep(1)

        clientK = pow(a, b, self.p)
        print("[✓] Shared key: {}".format(clientK))
