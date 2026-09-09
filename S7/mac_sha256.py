import sys
import os
from cryptography.hazmat.primitives import hashes

def setup(fkey):
    key = os.urandom(32)
    with open(fkey, "wb") as f:
        f.write(key)

def mac(fich, fkey):
    with open(fkey, "rb") as f:
        key = f.read()
    
    with open(fich, "rb") as f:
        msg = f.read()
    
    digest = hashes.Hash(hashes.SHA256())
    digest.update(key + msg)

    tag = digest.finalize()

    with open(fich + ".mac", "wb") as f:
        f.write(tag)


def ver(fich, fkey):
    with open(fkey, "rb") as f:
        key = f.read()
    
    with open(fich, "rb") as f:
        msg = f.read()
    
    with open(fich + ".mac", "rb") as f:
        tag = f.read()

    digest = hashes.Hash(hashes.SHA256())
    digest.update(key + msg)

    tag_check = digest.finalize()

    print(tag_check == tag)


def main():

    if len(sys.argv) < 3:
        print("Usage:")
        print("setup <fkey>")
        print("mac <fich> <fkey>")
        print("ver <fich> <fkey>")
        sys.exit(1)

    op = sys.argv[1]

    if op == "setup":
        setup(sys.argv[2])

    elif op == "mac":
        mac(sys.argv[2], sys.argv[3])

    elif op == "ver":
        ver(sys.argv[2], sys.argv[3])

    else:
        print("Invalid operation")


if __name__ == "__main__":
    main()