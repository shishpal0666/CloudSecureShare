import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

# Load recipient's private key
with open("keys/recipient_private_key.pem", "rb") as f:
    recipient_private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

# Load sender's ephemeral public key
with open("keys/ephemeral_public_key.pem", "rb") as f:
    ephemeral_public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

# Derive shared key
shared_key = recipient_private_key.exchange(ec.ECDH(), ephemeral_public_key)

# Derive key for AES key decryption
with open("files/sample.txt.key.enc", "rb") as f:
    key_data = f.read()
iv_key = key_data[:16]
encrypted_aes_key = key_data[16:]

derived_key = HKDF(
    algorithm=hashes.SHA256(), length=32, salt=None,
    info=b"handshake data", backend=default_backend()
).derive(shared_key)

cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv_key))
dec = cipher.decryptor()
aes_key = dec.update(encrypted_aes_key) + dec.finalize()

# Decrypt file
with open("files/sample.txt.enc", "rb") as f:
    file_data = f.read()
iv = file_data[:16]
ciphertext = file_data[16:]

cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
dec = cipher.decryptor()
decrypted = dec.update(ciphertext) + dec.finalize()

with open("files/sample_decrypted.txt", "wb") as f:
    f.write(decrypted)

print("✅ File decrypted.")