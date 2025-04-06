# 🔐🌩 CloudSecureShare -> Secure File Sharing System — Cloud Computing Perspective
---

## 🧭 Objective
The system demonstrates **secure, privacy-preserving file sharing over the cloud**, addressing data confidentiality, secure key exchange, and access control — key concerns in **Cloud Computing** environments where data owners do not control the storage infrastructure.

---

## 📊 Workflow Overview

### 1. Key Generation (Automated – Local Device)
- ECC (Elliptic Curve Cryptography) keys are generated:
  - `recipient_private_key.pem`
  - `recipient_public_key.pem`
- This simulates the **user’s cryptographic identity** for cloud interactions.
- Performed **locally** for security, ensuring the private key is never exposed.

#### 🔧 Code Trigger  
```bash
python keygen/generate_keys.py
```
(Automatically called inside `test_workflow.py`)

---

### 2. File Encryption (Client-Side - Local)
- A **random AES symmetric key** is generated.
- The file (e.g., `sample.txt`) is encrypted using AES (fast & secure for bulk data).
- The AES key itself is **encrypted using ECC + HKDF-derived shared key** to ensure **confidential key exchange**.
- The **ephemeral ECC key** adds forward secrecy.

#### 🔐 Security Concepts:
- Combines **asymmetric ECC (for key exchange)** with **symmetric AES (for data encryption)**.
- Ensures **end-to-end encryption** before cloud upload.

---

### 3. Cloud Upload (AWS S3 - Cloud)
- Encrypted files are uploaded to the **cloud (Amazon S3)**:
  - `sample.txt.enc` → encrypted file  
  - `sample.txt.key.enc` → encrypted AES key  
  - `ephemeral_public_key.pem` → public part of temporary ECC key for decryption  

#### ☁️ Cloud Role:
- **Storage-as-a-Service (SaaS/IaaS)** used here.
- Demonstrates **secure cloud storage** where the cloud is **untrusted but usable**, since encryption is handled on the client side.

#### 🔧 Code:
```python
s3_client.upload_file("files/sample.txt.enc", bucket_name, "sample.txt.enc")
```

---

### 4. Cloud Download (AWS S3 - Cloud)
- Receiver downloads the 3 files.
- Decryption is performed locally using their `recipient_private_key.pem`.

---

### 5. File Decryption (Client-Side - Local)
- ECC + HKDF is used again to derive the same shared key.
- The AES key is decrypted using this shared key.
- Finally, the file is decrypted using the recovered AES key.

---

## 📂 Code Flow Summary

```bash
test_workflow.py
├── generate_keys()              # ECC keypair generation
├── encrypt_file_and_key()       # AES + ECC + HKDF encryption
├── upload_to_s3()               # Upload encrypted files to cloud
├── download_from_s3()           # Retrieve encrypted data from cloud
└── decrypt_file()               # Reconstruct AES key, decrypt file
```

---

## 🔐🧪 Usage Scenario (Cloud Computing Context)

| Feature                     | Traditional Cloud File Upload | Your Secure File Sharing System |
|----------------------------|-------------------------------|----------------------------------|
| Encryption                 | Optional or server-side       | Mandatory, client-side           |
| Key Exchange               | Not secure or centralized     | Secure ECC-based peer-to-peer    |
| Cloud Trust Assumption     | Must trust provider           | Zero trust model                 |
| Data Confidentiality       | May be exposed to provider    | Fully encrypted before upload    |
| Identity & Authentication  | Password or OAuth             | Cryptographic keys (ECC)         |
| Flexibility                | Limited                       | End-to-end control               |
| Forward Secrecy            | Rare                          | ✅ Ephemeral ECC keys used       |

---

## 🧠 Why this is Ideal for Cloud Computing

- **Data Ownership:** User has full control over encryption keys — aligns with **confidential computing** principles.
- **No Server-Side Trust:** Data can be safely stored on **public clouds** (e.g., AWS) without relying on provider security.
- **Portable Security:** Files are self-contained and secured for any cloud provider.
- **Ephemeral Keys:** Protect against future key compromise — an advanced concept in secure cloud sharing.

---

## 🔄 Possible Enhancements (for future research/demo)
- Add **access control via blockchain or smart contracts**
- Enable **multi-user key sharing using proxy re-encryption**
- Support **mobile/cloud-based decryption apps**
- Add **metadata protection** (file names, sizes)
- Integrate **attribute-based encryption (ABE)** for policy-based access in multi-cloud environments
