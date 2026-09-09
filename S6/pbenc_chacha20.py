import sys
import os
from getpass import getpass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt(fich):
    password = getpass("Enter password: ")
    salt = os.urandom(16)
    nonce = os.urandom(16)

    key = derive_key(password, salt)

    with open(fich, "rb") as f:
        plaintext = f.read()
    
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext)

    with open(fich + ".enc", "wb") as f:
        f.write(salt + nonce + ciphertext)


def decrypt(fich):
    password = getpass("Enter password: ")

    with open(fich, "rb") as f:
        data = f.read()

    salt = data[:16]
    nonce = data[16:32]
    ciphertext = data[32:]

    key = derive_key(password, salt)

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext)

    with open(fich + ".dec", "wb") as f:
        f.write(plaintext)


def main():
    if len(sys.argv) < 3:
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