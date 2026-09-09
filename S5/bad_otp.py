import sys
import random

def bad_prng(n):
    """an INSECURE pseudo-random number generator"""
    random.seed(random.randbytes(2))
    return random.randbytes(n)

def xor_bytes(data, key):
    res = bytearray()

    for i in range(len(data)):
        res.append(data[i] ^ key[i])

    return res


def main():

    if len(sys.argv) != 4:
        print("Usage: python3 bad_otp.py setup N KEYFILE | enc FILE KEYFILE | dec FILE KEYFILE")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "setup":

        n = int(sys.argv[2])
        keyfile = sys.argv[3]

        key = bad_prng(n)
        with open(keyfile, "wb") as f:
            f.write(key)

    elif mode == "enc":

        msgfile = sys.argv[2]
        keyfile = sys.argv[3]

        with open(msgfile, "rb") as f:
            msg = f.read()

        with open(keyfile, "rb") as f:
            key = f.read()

        cipher = xor_bytes(msg, key)

        outfile = msgfile + ".enc"

        with open(outfile, "wb") as f:
            f.write(cipher)

    elif mode == "dec":

        cipherfile = sys.argv[2]
        keyfile = sys.argv[3]

        with open(cipherfile, "rb") as f:
            cipher = f.read()

        with open(keyfile, "rb") as f:
            key = f.read()

        msg = xor_bytes(cipher, key)

        outfile = cipherfile + ".dec"

        with open(outfile, "wb") as f:
            f.write(msg)

    else:
        print("Invalid mode")
        sys.exit(1)


if __name__ == "__main__":
    main()