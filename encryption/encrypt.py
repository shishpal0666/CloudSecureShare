import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode

# Load recipient's public key
with open("keys/recipient_public_key.pem", "rb") as f:
    recipient_public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

# Generate AES key and IV
aes_key = os.urandom(32)
iv = os.urandom(16)

# Encrypt file using AES
with open("files/sample.txt", "rb") as f:
    plaintext = f.read()

cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

with open("files/sample.txt.enc", "wb") as f:
    f.write(iv + ciphertext)

# ECC key exchange
ephemeral_private_key = ec.generate_private_key(ec.SECP384R1())
ephemeral_public_key = ephemeral_private_key.public_key()
shared_key = ephemeral_private_key.exchange(ec.ECDH(), recipient_public_key)

# Derive key to encrypt AES key
derived_key = HKDF(
    algorithm=hashes.SHA256(), length=32, salt=None,
    info=b"handshake data", backend=default_backend()
).derive(shared_key)

cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv))
enc = cipher.encryptor()
encrypted_aes_key = enc.update(aes_key) + enc.finalize()

with open("files/sample.txt.key.enc", "wb") as f:
    f.write(iv + encrypted_aes_key)

# Save ephemeral public key
with open("keys/ephemeral_public_key.pem", "wb") as f:
    f.write(ephemeral_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    
print("✅ File and AES key encrypted.")
