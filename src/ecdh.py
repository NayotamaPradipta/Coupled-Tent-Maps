# Implementation of ECDH Key exchange 
import os 
from ecc import scalar_multiplication
from Crypto.Util.number import bytes_to_long

# Curve parameters for secp192r1 (P-192)
p = int('fffffffffffffffffffffffffffffffeffffffffffffffff', 16)
a = int('fffffffffffffffffffffffffffffffefffffffffffffffc', 16)
# Generator point
Gx = int('188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012', 16)
Gy = int('07192b95ffc8da78631011ed6b24cdd573f977a11e794811', 16)
# Order of the generator (192 bit)
n = int('ffffffffffffffffffffffff99def836146bc9b1b4d22831', 16)

def generate_key_pair():
    # Generate a random 192-bit private key
    privateKey = bytes_to_long(os.urandom(24)) % (n - 1) + 1
    # Calculate public key
    publicKey = scalar_multiplication(privateKey, (Gx, Gy), p, a)
    return {
        'privateKey': hex(privateKey),
        'publicKey': (hex(publicKey[0]), hex(publicKey[1]))
    }

def compute_shared_key(privateKey, publicKey):
    privateKey = int(privateKey, 16) 
    publicKey = (int(publicKey[0], 16), int(publicKey[1], 16))
    sharedPoint = scalar_multiplication(privateKey, publicKey, p, a)
    return hex(sharedPoint[0])

if __name__ == "__main__": 
    key_pair = generate_key_pair()
    print("Generated key pair:", key_pair)
    peer_key_pair = generate_key_pair()
    shared_key = compute_shared_key(key_pair['privateKey'], peer_key_pair['publicKey'])
    print("Shared key:", shared_key)