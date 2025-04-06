import os
import subprocess
from s3_upload_download.upload import upload_file
from s3_upload_download.download import download_file
# Run key generation script
subprocess.run(["python", os.path.join("keygen", "generate_keys.py")])


# Make sure files directory exists
os.makedirs("files", exist_ok=True)
os.makedirs("keys", exist_ok=True)

print("✅ ECC Keys generated successfully.")
subprocess.run(["python", "keygen/generate_keys.py"])

print("✅ File and AES key encrypted.")
subprocess.run(["python", "encryption/encrypt.py"])

# Upload to S3
upload_file("files/sample.txt.enc")
upload_file("files/sample.txt.key.enc")
upload_file("keys/ephemeral_public_key.pem")

# Download from S3
download_file("sample.txt.enc")
download_file("sample.txt.key.enc")
download_file("ephemeral_public_key.pem")

print("✅ File decrypted.")
subprocess.run(["python", "encryption/decrypt.py"])

print("✅ Full encryption/decryption + S3 cycle completed!")
