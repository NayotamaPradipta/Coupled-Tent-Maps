# Implementation of Coupled Tent Maps 
import numpy as np 
import cv2 
from ecdh import generate_key_pair, compute_shared_key 

# Initial parameters using shared key through ECDH key exchange
sender_keys = generate_key_pair()
receiver_keys = generate_key_pair()
shared_key_receiver = compute_shared_key(receiver_keys['privateKey'], sender_keys['publicKey'])
shared_key_sender = compute_shared_key(sender_keys['privateKey'], receiver_keys['publicKey'])

def modify_key(shared_key): 
    modified_key = shared_key.strip('0x')[::-1]
    shared_key_int = int(modified_key, 16)
    initial_value2 = shared_key_int % 256 / 255
    return initial_value2


def init_tent_map_params(shared_key):
    shared_key_int = int(shared_key, 16)
    initial_value = shared_key_int % 256 / 255 
    slope = 1.9
    return initial_value, slope 

def tent_map(length, initial_value1, initial_value2, slope):
    sequence1 = np.zeros(length)
    sequence2 = np.zeros(length)
    sequence1[0] = initial_value1
    sequence2[0] = initial_value2
    alpha = 0.1
    for i in range(1, length):
        if sequence1[i-1] < 0.5: 
            sequence1[i] = slope * sequence1[i-1]
        else: 
            sequence1[i] = slope * (1- sequence1[i-1])


        # Coupling 
        if sequence2[i-1] < 0.5: 
            sequence2[i] = slope * (sequence2[i-1] + alpha * sequence1[i-1]) % 1
        else: 
            sequence2[i] = slope * (1- (sequence2[i-1] + alpha * sequence1[i-1])) % 1

    return sequence1, sequence2

img = cv2.imread('../images/sample/PII.png', cv2.IMREAD_GRAYSCALE)
if img is None: 
    raise FileNotFoundError("Image file not found at specified path")

pixels = img.flatten()
initial_value1, slope = init_tent_map_params(shared_key_sender)
initial_value2 = modify_key(shared_key_sender)
chaotic_sequence1, chaotic_sequence2 = tent_map(len(pixels), initial_value1, initial_value2, slope)

# Encrypt 
encrypted_pixels = (pixels + (chaotic_sequence1 * 255).astype(int) + (chaotic_sequence2 * 255).astype(int)) % 256
encrypted_image = encrypted_pixels.reshape(img.shape)

cv2.imwrite('../images/encrypted/PII_encrypted.png', encrypted_image)
# Decrypt 

encrypted_image_loaded = cv2.imread('../images/encrypted/PII_encrypted.png', cv2.IMREAD_GRAYSCALE)

decrypted_pixels = (encrypted_pixels - (chaotic_sequence1 * 255).astype(int) - (chaotic_sequence2 * 255).astype(int)) % 256
decrypted_image = decrypted_pixels.reshape(img.shape)


cv2.imwrite('../images/decrypted/PII_decrypted.png', decrypted_image)
