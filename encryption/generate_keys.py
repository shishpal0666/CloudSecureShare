# Directory: encryption/generate_keys.py
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

for user in ['sender', 'recipient']:
    private_key = ec.generate_private_key(ec.SECP384R1())
    public_key = private_key.public_key()

    with open(f'keys/{user}_private_key.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        ))

    with open(f'keys/{user}_public_key.pem', 'wb') as f:
        f.write(public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ))

print("✅ ECC Keys generated successfully.")