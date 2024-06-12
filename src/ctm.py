# Implementation of Coupled Tent Maps 
import numpy as np 
import cv2 
import time 
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
    initial_value1 = shared_key_int % 256 / 255 
    initial_value2 = modify_key(shared_key)
    slope = 1.9
    return initial_value1, initial_value2, slope 

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

def encrypt(pixels, chaotic_sequence1, chaotic_sequence2, shape): 
    encrypted_pixels = (pixels + (chaotic_sequence1 * 255).astype(int) + (chaotic_sequence2 * 255).astype(int)) % 256
    return encrypted_pixels.reshape(shape)

def decrypt(pixels, chaotic_sequence1, chaotic_sequence2, shape): 
    decrypted_pixels = (pixels - (chaotic_sequence1 * 255).astype(int) - (chaotic_sequence2 * 255).astype(int)) % 256
    return decrypted_pixels.reshape(shape)


if __name__ == "__main__": 

    # Encrypt 
    img = cv2.imread('../images/sample/PII.png', cv2.IMREAD_GRAYSCALE)
    if img is None: 
        raise FileNotFoundError("Image file not found at specified path")

    pixels = img.flatten()

    start_time_encryption = time.time()
    initial_value1, initial_value2, slope = init_tent_map_params(shared_key_sender)
    chaotic_sequence1, chaotic_sequence2 = tent_map(len(pixels), initial_value1, initial_value2, slope)

    encrypted_image = encrypt(pixels, chaotic_sequence1, chaotic_sequence2, img.shape)
    encryption_time = time.time() - start_time_encryption

    print(f"Encryption time: {encryption_time:.2f} seconds")

    cv2.imwrite('../images/encrypted/PII_encrypted.png', encrypted_image)

    # Decrypt 
    
    encrypted_image_loaded = cv2.imread('../images/encrypted/PII_encrypted.png', cv2.IMREAD_GRAYSCALE)
    d_pixels = encrypted_image_loaded.flatten()

    start_time_decryption = time.time()
    d_init_val1, d_init_val2, d_slope = init_tent_map_params(shared_key_receiver)
    d_chaotic_sequence1, d_chaotic_sequence2 = tent_map(len(d_pixels), d_init_val1, d_init_val2, d_slope)
    decrypted_image = decrypt(d_pixels, d_chaotic_sequence1, d_chaotic_sequence2, encrypted_image_loaded.shape)
    decryption_time = time.time() - start_time_decryption
    print(f"Decryption time: {decryption_time:.2f} seconds")

    cv2.imwrite('../images/decrypted/PII_decrypted.png', decrypted_image)
