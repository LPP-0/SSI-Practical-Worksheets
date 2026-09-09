import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def setup(fkey):
    key = os.urandom(32)
    with open(fkey, 'wb') as f:
        f.write(key)


def encrypt(fich, fkey):
    with open(fkey, 'rb') as f:
        key = f.read()

    with open(fich, 'rb') as f:
        plaintext = f.read()
    
    iv = os.urandom(16)

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    with open(fich + ".enc", 'wb') as f:
        f.write(iv + ciphertext)


def decrypt(fich, fkey):
    with open(fkey, 'rb') as f:
        key = f.read()

    with open(fich, 'rb') as f:
        data = f.read()

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()

    with open(fich + ".dec", 'wb') as f:
        f.write(plaintext)


def main():
    if len(sys.argv) < 3:
        print("Usage:\n setup <fkey>\n enc <fich> <fkey>\n dec <fich> <fkey>")
        return
    
    op = sys.argv[1]
    if op == 'setup':
        setup(sys.argv[2])
    elif op == 'enc':
        encrypt(sys.argv[2], sys.argv[3])
    elif op == 'dec':
        decrypt(sys.argv[2], sys.argv[3])
    else:
        print("Invalid operation")

if __name__ == "__main__":
    main()