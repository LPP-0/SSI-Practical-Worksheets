import sys
import random

def xor_bytes(data, key):
    res = bytearray()

    for i in range(len(data)):
        res.append(data[i] ^ key[i])

    return res


def main():

    if len(sys.argv) < 4:
        print("Usage: python3 bad_otp_attack.py KEYLEN CRIPTOGRAMA WORD1 [WORD2...]")
        sys.exit(1)

    key_len = int(sys.argv[1])
    cryptofile = sys.argv[2]
    words = sys.argv[3:]

    with open(cryptofile, "rb") as f:
        crypto = f.read()

    for seed in range(2**16):

        random.seed(seed.to_bytes(2, "big"))
        key = random.randbytes(key_len)

        msg = xor_bytes(crypto, key)

        try:
            text = msg.decode("utf-8")
        except:
            continue

        for w in words:
            if w in text:
                print(text)
                return


if __name__ == "__main__":
    main()