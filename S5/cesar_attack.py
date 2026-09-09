import sys

def preproc(s):
    l = []
    for c in s:
        if c.isalpha():
            l.append(c.upper())
    return "".join(l)


def cesar_dec(key, msg):
    res = []
    k = ord(key.upper()) - ord('A')

    for c in msg:
        p = ord(c) - ord('A')
        c_dec = (p - k) % 26
        res.append(chr(c_dec + ord('A')))
    
    return "".join(res)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 cesar_attack.py CRIPTOGRAMA WORD1 [WORD2 ...]")
        sys.exit(1)
    
    criptograma = preproc(sys.argv[1])
    words = [preproc(w) for w in sys.argv[2:]]

    for k in range(26):
        key = chr(ord('A') + k)
        texto = cesar_dec(key, criptograma)

        for w in words:
            if w in texto:
                print(key)
                print(texto)
                return
    
    return

if __name__ == "__main__":
    main()