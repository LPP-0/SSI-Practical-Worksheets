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

    if len(sys.argv) < 4:
        print("Usage: python3 vigenere_attack.py KEYLEN CRIPTOGRAMA WORD1 [WORD2...]")
        sys.exit(1)

    key_len = int(sys.argv[1])
    criptograma = preproc(sys.argv[2])
    words = [preproc(w) for w in sys.argv[3:]]

    key = ""

    for i in range(key_len):
        part = criptograma[i::key_len]

        best_key = 'A'
        best_score = -1

        for k in range(26):

            guess_key = chr(ord('A') + k)
            dec = cesar_dec(guess_key, part)

            score = 0
            for c in dec:
                if c in "AEOS":
                    score += 1

            if score > best_score:
                best_score = score
                best_key = guess_key

        key += best_key

    texto = vigenere_dec(key, criptograma)

    for w in words:
        if w in texto:
            print(key)
            print(texto)
            return


if __name__ == "__main__":
    main()