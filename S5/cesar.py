import sys

def preproc(s):
    l = []
    for c in s:
        if c.isalpha():
            l.append(c.upper())
    return "".join(l)

def cesar_enc(key, msg):
    res = []
    k = ord(key.upper()) - ord('A')

    for c in msg:
        p = ord(c) - ord('A')
        c_enc = (p + k) % 26
        res.append(chr(c_enc + ord('A')))
    
    return "".join(res)

def cesar_dec(key, msg):
    res = []
    k = ord(key.upper()) - ord('A')

    for c in msg:
        p = ord(c) - ord('A')
        c_dec = (p - k) % 26
        res.append(chr(c_dec + ord('A')))
    
    return "".join(res)


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 cesar.py enc|dec KEY MESSAGE")
        sys.exit(1)

    mode = sys.argv[1]
    key = sys.argv[2]
    msg = sys.argv[3]

    msg = preproc(msg)

    if mode == "enc":
        print(cesar_enc(key, msg))
    elif mode == "dec":
        print(cesar_dec(key, msg))
    else:
        print("Invalid mode: use enc or dec")
        sys.exit(1)

if __name__ == "__main__":
    main()