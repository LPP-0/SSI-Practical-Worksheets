import sys

def preproc(s):
    l = []
    for c in s:
        if c.isalpha():
            l.append(c.upper())
    return "".join(l)

def vigenere_enc(key, msg):
    res = []
    key_len = len(key)

    for i, c in enumerate(msg):
        p = ord(c) - ord('A')
        k = ord(key[i % key_len]) - ord('A')
        c_enc = (p + k) % 26
        res.append(chr(c_enc + ord('A')))
    
    return "".join(res)

def vigenere_dec(key, msg):
    res = []
    key_len = len(key)

    for i, c in enumerate(msg):
        p = ord(c) - ord('A')
        k = ord(key[i % key_len]) - ord('A')
        c_dec = (p - k) % 26
        res.append(chr(c_dec + ord('A')))
    
    return "".join(res)


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 vigenere.py enc|dec KEY MESSAGE")
        sys.exit(1)

    mode = sys.argv[1]
    key = preproc(sys.argv[2])
    msg = preproc(sys.argv[3])

    if mode == "enc":
        print(vigenere_enc(key, msg))
    elif mode == "dec":
        print(vigenere_dec(key, msg))
    else:
        print("Invalid mode. Use enc or dec.")
        sys.exit(1)

if __name__ == "__main__":
    main()
