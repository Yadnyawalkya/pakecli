# pakecli: A command line tool for Password-authenticated key exchange

## Options
```
$ pakecli --help
Usage: pakecli [OPTIONS]

Options:
  -m, --method TEXT    Select protocol ('jpake' or 'speke')
  -r, --role TEXT      Type of role ('server' or 'client')
  -p, --prime INTEGER  Prime number in bits (default 32 bits)
  -s, --secret TEXT    Low entropy shared-secret
  --help               Show this message and exit.
```

## Installation
```
# Create virtual envirement 
$ virtualenv env

# Activate virtual envirement
$ soure env/bin/activate

# Install pakecli command line tool
$ pip install --editable .
```

## Usage
### On server side
```
$ pakecli --method jpake --role server --prime 64 --secret hello
[-] Server has generated random values...
[-] Non-Interactive Zero Knowledge (NI-ZKP) Proof
    => Generated...
[-] High entropy shared key for server
    => Generated...
    => Sent to client...
    => Received from client...
[✓] Shared key verified on server side !!!
=> 4853078800621906277
```

### On client side
```
$ pakecli --method jpake --role client --prime 64 --secret hello
[-] Client has generated random values...
[-] Non-Interactive Zero Knowledge (NI-ZKP) Proof
    => Generated...
[-] High entropy shared key for client
    => Generated...
    => Received from server...
    => Sent to server...
[✓] Shared key verified on server side !!!
=> 4853078800621906277
```

### Todo
- [x] J-Pake
- [ ] SPEKE
