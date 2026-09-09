import sys
import os
from getpass import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


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
    nonce = os.urandom(12)

    key = derive_key(password, salt)

    with open(fich, "rb") as f:
        plaintext = f.read()

    aesgcm = AESGCM(key)

    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    with open(fich + ".enc", "wb") as f:
        f.write(salt + nonce + ciphertext)


def decrypt(fich):
    password = getpass("Enter password: ")

    with open(fich, "rb") as f:
        data = f.read()

    salt = data[:16]
    nonce = data[16:28]
    ciphertext = data[28:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    except Exception:
        print("Decryption failed (invalid tag or password)")
        return

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