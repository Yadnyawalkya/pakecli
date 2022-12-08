import random
import hashlib
import socket
import time
import sys
import hashlib
import random

from Crypto.Util.number import getPrime
from Crypto.Random import get_random_bytes

from libnum import invmod

class spekeServer:
    def __init__(self, p, g):
        self.p = p
        self.g = g

    def validate_key(self, p, g):
        s = socket.socket()
        port = 11122        
        s.bind(('', port))
        s.listen(5)
        c, addr = s.accept()

        self.p = p
        self.g = g

        c.send(str(self.p).encode())
        time.sleep(1)
        c.send(str(self.g).encode())
        time.sleep(1)

        a = random.randint(0, self.p-1)
        server_to_send = pow(self.g, a, self.p)
        c.send(str(server_to_send).encode())
        print("    => Sent to client...")
        time.sleep(1)

        b = int(c.recv(1024).decode())
        print("    => Received from client...")
        time.sleep(1)

        serverK = pow(b, a, self.p)
        print("[✓] Shared key: {}".format(serverK))
