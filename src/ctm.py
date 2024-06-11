# Implementation of Coupled Tent Maps 
from ecdh import generate_key_pair, compute_shared_key 

# Initial parameters using shared key through ECDH key exchange
sender_keys = generate_key_pair()
receiver_keys = generate_key_pair()
shared_key_receiver = compute_shared_key(receiver_keys['privateKey'], sender_keys['publicKey'])
shared_key_sender = compute_shared_key(sender_keys['privateKey'], receiver_keys['publicKey'])
print(shared_key_receiver == shared_key_sender)