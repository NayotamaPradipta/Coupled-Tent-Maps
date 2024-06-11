# Implementation of Coupled Tent Maps 
import numpy as np 
import cv2 
from ecdh import generate_key_pair, compute_shared_key 

# Initial parameters using shared key through ECDH key exchange
sender_keys = generate_key_pair()
receiver_keys = generate_key_pair()
shared_key_receiver = compute_shared_key(receiver_keys['privateKey'], sender_keys['publicKey'])
shared_key_sender = compute_shared_key(sender_keys['privateKey'], receiver_keys['publicKey'])

def init_tent_map_params(shared_key):
    shared_key_int = int(shared_key, 16)
    initial_value = shared_key_int % 256 / 255 
    slope = 1.9
    return initial_value, slope 

def tent_map(length, initial_value, slope):
    sequence = np.zeros(length)
    sequence[0] = initial_value
    for i in range(1, length):
        if sequence[i-1] < 0.5: 
            sequence[i] = slope * sequence[i-1]
        else: 
            sequence[i] = slope * (1- sequence[i-1])
    return sequence 

img = cv2.imread('../images/sample/PII.png', cv2.IMREAD_GRAYSCALE)
pixels = img.flatten()

initial_value, slope = init_tent_map_params(shared_key_sender)
chaotic_sequence = tent_map(len(pixels), initial_value, slope)
encrypted_pixels = (pixels + (chaotic_sequence * 255).astype(int)) % 256
encrypted_image = encrypted_pixels.reshape(img.shape)

decrypted_pixels = (encrypted_pixels - (chaotic_sequence * 255).astype(int)) % 256
decrypted_image = decrypted_pixels.reshape(img.shape)

cv2.imwrite('../images/encrypted/PII_encrypted.png', encrypted_image)
cv2.imwrite('../images/decrypted/PII_decrypted.png', decrypted_image)
