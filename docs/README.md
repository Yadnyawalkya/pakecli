# J-PAKE

The Password Authenticated Key Exchange by Juggling (or J-PAKE) is a password-authenticated key agreement protocol, proposed by Feng Hao and Peter Ryan. This protocol allows two parties to establish private and authenticated communication solely based on their shared (low-entropy) password without requiring a Public Key Infrastructure. It provides mutual authentication to the key exchange, a feature that is lacking in the Diffie–Hellman key exchange protocol.

## How J-PAKE works

### Round 1

Alice then generates two random values: x1 and x2. These are kept secret, and where Alice will send the following to Bob:
```
g^x1 (mod p)
g^x2 (mod p)
```

Alice will also provide a Non-Interactive Zero Knowledge (NI-ZKP) that she knows x1 and x2. Bob then generates two random values: x3 and x4. These are kept secret, and where Bob will send the following to Alice:
```
g^x3 (mod p)
g^x4 (mod p)
```

Alice will also provide a Non-Interactive Zero Knowledge (NI-ZKP) Proof that she knows x3 and x4.

### Round 2
Alice then calculates the following and sends to Bob: 
```
A = (g^x1 * g^x3 * g^x4)^x2s (mod p)
```

Bob then calculates the following and sends to Alice: 
```
B = (g^x1 * g^x2 * g^x3)^x4s (mod p)
```

Alice then calculates the shared key as:
```
K = (B(g^x4)^x2 * s)^x2
```

Bob then calculates the shared key as:
```
K = (A(g^x2)^x4 * s)^x4
```

