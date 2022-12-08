import click
import hashlib
from jpakeServer import jpakeServer as js
from jpakeClient import jpakeClient as jc
from spekeServer import spekeServer as ss
from spekeClient import spekeClient as sc
from Crypto.Util.number import getPrime
from Crypto.Random import get_random_bytes

def error():
    # returns error msg
    return "This option does not exists!"

def check_prime(n):
    # check if number is prime or not
    return ([(n % j) for j in range(2, int(n**0.5)+1)]) and n>1

def get_prime(p):
    # generate prime number
    return getPrime(p, randfunc=get_random_bytes)

@click.command()
@click.option('-m', '--method', type=str, help="Select protocol ('jpake' or 'speke')")
@click.option('-r', '--role', type=str, help="Type of role ('server' or 'client')")
@click.option('-p', '--prime', default=32, help="Prime bits (default 32 bits)")
@click.option('-s', '--secret', type=str, default=1, help="Low entropy shared-secret")
def pake(method, role, prime, secret):

    if check_prime(prime):
        pass
    else:
        print("[x] {} is not a prime number (bits)".format(prime))
        exit()

    if method == "jpake":
        g = 3
        p = get_prime(prime)
        js.secret, jc.secret = secret, secret
        js.g, jc.g = g, g
        if role == "server":
            js.validate_key(js, p)
        elif role == "client":
            jc.validate_key(jc)
    elif method == "speke":
        p = get_prime(prime)
        g = pow(int(hashlib.sha1(secret.encode()).hexdigest(), 16),2,p)
        if role == "server":
            ss.validate_key(ss, p, g)
        elif role == "client":
            sc.validate_key(sc)
    else:
        error()


if __name__ == '__main__':
    pake()
