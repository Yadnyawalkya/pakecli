import random
import hashlib
import socket
import time

from libnum import invmod

class jpakeClient:
    def __init__(self, p, g, secret, salt):
        self.p = p
        self.g = g
        self.secret = secret
        self.salt = salt
    
    def generate_two_values(self):
        # generates two random values (this are kept secret)
        self.salt=int(hashlib.md5(self.secret.encode()).hexdigest(),16)
        x3 = random.randint(0, self.p-1)
        x4 = random.randint(0, self.p-1)
        print("[-] Client has generated random values...")
        time.sleep(2)
        # generates Non-Interactive Zero Knowledge
        g_x3 = pow(self.g,x3,self.p)
        g_x4 = pow(self.g,x4,self.p)
        print("[-] Non-Interactive Zero Knowledge (NI-ZKP) Proof")
        print("    => Generated...")
        time.sleep(2)
        return (x4, g_x3, g_x4)

    def generate_B(self, g_x1, g_x2, g_x3, x4):
        # generates first stage to send it to server
        B = pow(g_x1*g_x2*g_x3,x4*self.salt,self.p)
        return B

    def generate_inverse(self, g_x2, x4):
        # generates inverse for shared key
        K_inv2 = invmod(pow(g_x2,x4*self.salt,self.p),self.p)
        return K_inv2
    
    def generate_key(self, A, K_inv2, x4):
        # generates high entropy shared key
        print("[-] High entropy shared key for client")
        print("    => Generated...")
        time.sleep(2)
        client_key = pow(A*K_inv2,x4,self.p)
        return client_key

    def validate_key(self):
        # create socket and connect to host server
        s = socket.socket()        
        port = 12345               
        s.connect(('127.0.0.1', port))

        # receive randomly generated prime from the server
        self.p = int(s.recv(1024).decode())

        # send and receive first stage
        g_x1, g_x2 = [int (i) for i in s.recv(1024).decode().split(",")]
        x4, g_x3, g_x4 = self.generate_two_values(self)
        first_response = "{},{}".format(g_x3, g_x4)
        s.send(first_response.encode())
        K_inv2 = self.generate_inverse(self, g_x2, x4)
        A = int(s.recv(1024).decode())
        B = self.generate_B(self, g_x1, g_x2, g_x3, x4)
        s.send(str(B).encode())
        client_key = self.generate_key(self, A, K_inv2, x4)

        # send and receive shared key
        server_key = int(s.recv(1024).decode())
        print("    => Received from server...")
        time.sleep(2)
        s.send(str(client_key).encode())
        print("    => Sent to server...")
        time.sleep(2)

        # validate shared key
        if server_key == client_key:
            print("[✓] Shared key verified on server side !!!")
            print("=> {}".format(server_key))
            time.sleep(2)

        s.close()
