import hashlib
import hmac

def sha256_hex_bytes(bytes_data):
    # no encode() because we are already passing bytes
    return hashlib.sha256(bytes_data).hexdigest()

def xor_crypt_or_decrypt(plain_text, key):
    pt = plain_text
    len_key = len(key)
    encoded = []
    for i in range(0, len(pt)):
        encoded.append(pt[i] ^ key[i % len_key])
    return bytes(encoded) # returning as bytes as it will be used so

def hmac_sign(secret, message_bytes):
    # fix: combined data stays as bytes, then gets converted to hex string
    inner_hash = sha256_hex_bytes(secret + message_bytes)
    outer_hash = sha256_hex_bytes(secret + inner_hash.encode('utf-8'))
    return outer_hash

def constant_time_equals(hash1, hash2):
    return hmac.compare_digest(hash1, hash2)

# --- setup ---
plain_text = input("Enter plain text: ").encode('utf-8')
key = b'liran'

# --- sending msg (Sender Side) ---
# encrypt the text
ciphertext_hex = xor_crypt_or_decrypt(plain_text, key)
# singing the ciphered text
sent_signed_tag = hmac_sign(key, ciphertext_hex)


# --- receiving message ---

# # simulation of attack: a hacker changes the ciphertext while sending
# ciphertext_hex = b"hacked_bytes_here"

# paradox solve: the receiver only uses the ciphertext and the key
# they do not need the original plain_text variable
expected_signed = hmac_sign(key, ciphertext_hex)

# verifying the tags match
isequal = constant_time_equals(sent_signed_tag, expected_signed)

if isequal:
    decrypted_text = xor_crypt_or_decrypt(ciphertext_hex, key).decode('utf-8')
    print("encrypted bytes:", ciphertext_hex)
    print("\ndecrypted text:\n" + decrypted_text)
else:
    print('stupid hacker tried to be smart')
