import random
import hashlib
import socket
import time

from libnum import invmod

class jpakeServer:
    def __init__(self, p, g, secret, salt):
        self.p = p
        self.g = g
        self.secret = secret
        self.salt = salt
    
    def generate_two_values(self):
        self.salt=int(hashlib.md5(self.secret.encode()).hexdigest(),16)
        # generates two random values (this are kept secret)
        x1 = random.randint(0, self.p-1)
        x2 = random.randint(0, self.p-1)
        print("[-] Server has generated random values...")
        time.sleep(1)
        # generates Non-Interactive Zero Knowledge
        g_x1 = pow(self.g,x1,self.p)
        g_x2 = pow(self.g,x2,self.p)
        print("[-] Non-Interactive Zero Knowledge (NI-ZKP) Proof")
        print("    => Generated...")
        time.sleep(1)
        return (x2, g_x1, g_x2)

    def generate_A(self, g_x1, g_x3, g_x4, x2):
        # generates first stage to send it to client
        A = pow(g_x1*g_x3*g_x4,x2*self.salt,self.p)
        return A

    def generate_inverse(self, g_x4, x2):
        # generates inverse for shared key
        K_inv1 = invmod(pow(g_x4,x2*self.salt,self.p),self.p)
        return K_inv1

    def generate_key(self, B, K_inv1, x2):
        # generates high entropy shared key
        print("[-] High entropy shared key for server")
        print("    => Generated...")
        time.sleep(2)
        server_key = pow(B*K_inv1,x2,self.p)
        return server_key

    def validate_key(self, p):
        # create socket and bind to port
        s = socket.socket()        
        port = 12345               
        s.bind(('', port))        
        s.listen(5)    
        c, addr = s.accept() 

        # send randomly generated prime to the client
        self.p = p
        c.send(str(self.p).encode())

        # send and receive first stage
        x2, g_x1, g_x2 = self.generate_two_values(self)
        first_response = "{},{}".format(g_x1, g_x2)
        c.send(first_response.encode())
        g_x3, g_x4 = [int (i) for i in c.recv(1024).decode().split(",")]
        A = self.generate_A(self, g_x1, g_x3, g_x4, x2)
        c.send(str(A).encode())
        K_inv1 = self.generate_inverse(self, g_x4, x2)
        B = int(c.recv(1024).decode())
        server_key = self.generate_key(self, B, K_inv1, x2)

        # send and receive shared key
        c.send(str(server_key).encode())
        print("    => Sent to client...")
        time.sleep(2)
        client_key = int(c.recv(1024).decode())
        print("    => Received from client...")
        time.sleep(2)

        # validate shared key
        if server_key == client_key:
            print("[✓] Shared key verified on server side !!!")
            print("=> {}".format(server_key))
            time.sleep(2)

        c.close()
