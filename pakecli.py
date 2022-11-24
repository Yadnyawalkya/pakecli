import click
from server import ServerSpace as ss
from client import ClientSpace as cs
from Crypto.Util.number import getPrime
from Crypto.Random import get_random_bytes

def error():
    # returns error msg
    return "This option does not exists!"

def check_prime(n):
    # check if number is prime or not
    return ([(n % j) for j in range(2, int(n**0.5)+1)]) and n>1

@click.command()
@click.option('-m', '--method', type=str, help="Select protocol ('jpake' or 'speke')")
@click.option('-r', '--role', type=str, help="Type of role ('server' or 'client')")
@click.option('-p', '--prime', default=32, help="Prime bits (default 32 bits)")
@click.option('-s', '--secret', type=str, default=1, help="Low entropy shared-secret")
def pake(method, role, prime, secret):
 
    g = 3
    p = getPrime(prime, randfunc=get_random_bytes)
    ss.secret, cs.secret = secret, secret
    ss.g, cs.g = g, g

    if check_prime(prime):
        pass
    else:
        print("[x] {} is not a prime number (bits)".format(prime))
        exit()

    if method == "jpake":
        pass
    elif method == "speke":
        print("Currently not implemented!")
    else:
        error()

    if role == "server":
        ss.validate_key(ss, p)
    elif role == "client":
        cs.validate_key(cs)

if __name__ == '__main__':
    pake()
