import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend


def setup(fkey):
    key = os.urandom(32)
    with open(fkey, "wb") as f:
        f.write(key)


def encrypt(fich, fkey):
    with open(fkey, "rb") as f:
        key = f.read()
    
    with open(fich, "rb") as f:
        plaintext = f.read()
    
    nonce = os.urandom(16)
    # nonce = b"\x00" * 16

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext)

    with open(fich + ".enc", "wb") as f:
        f.write(nonce + ciphertext)


def decrypt(fich, fkey):
    with open(fkey, "rb") as f:
        key = f.read()

    with open(fich, "rb") as f:
        data = f.read()

    nonce = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext)

    with open(fich + ".dec", "wb") as f:
        f.write(plaintext)


def main():
    if len(sys.argv) < 3:
        print("Usage:\n setup <fkey>\n enc <fich> <fkey>\n dec <fich> <fkey>")
        return

    op = sys.argv[1]

    if op == "setup":
        setup(sys.argv[2])

    elif op == "enc":
        encrypt(sys.argv[2], sys.argv[3])

    elif op == "dec":
        decrypt(sys.argv[2], sys.argv[3])

    else:
        print("Invalid operation")


if __name__ == "__main__":
    main()