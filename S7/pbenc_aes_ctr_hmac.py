import sys
import os
from getpass import getpass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac


def derive_keys(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=64, # AES + HMAC (32 + 32)
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    combined_key = kdf.derive(password.encode())
    return combined_key[:32], combined_key[32:]

def encrypt(fich):
    password = getpass("Enter password: ")
    salt = os.urandom(16)
    nonce = os.urandom(16)

    key_aes, key_hmac = derive_keys(password, salt)

    with open(fich, "rb") as f:
        plaintext = f.read()

    cipher = Cipher(algorithms.AES(key_aes), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    h = hmac.HMAC(key_hmac, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    tag = h.finalize()

    with open(fich + ".enc", "wb") as f:
        f.write(salt + nonce + ciphertext + tag)


def decrypt(fich):
    password = getpass("Enter password: ")

    with open(fich, "rb") as f:
        data = f.read()

    salt = data[:16]
    nonce = data[16:32]
    ciphertext = data[32:-32]
    tag = data[-32:]

    key_aes, key_hmac = derive_keys(password, salt)

    h = hmac.HMAC(key_hmac, hashes.SHA256(), backend=default_backend())
    h.update(ciphertext)
    try:
        h.verify(tag)
    except Exception:
        print("Invalid MAC")
        return

    cipher = Cipher(algorithms.AES(key_aes), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(fich + ".dec", "wb") as f:
            f.write(plaintext)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ["enc", "dec"]:
        print("Usage:\n enc <fich>\n dec <fich>")
        return

    op = sys.argv[1]

    if op == "enc":
        encrypt(sys.argv[2])

    elif op == "dec":
        decrypt(sys.argv[2])

    else:
        print("Invalid operation")


if __name__ == "__main__":
    main()