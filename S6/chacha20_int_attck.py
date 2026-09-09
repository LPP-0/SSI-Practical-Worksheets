import sys

def attack(fctxt, pos, ptxtAtPos, newPtxtAtPos):
    pos = int(pos)
    ptxt_bytes = ptxtAtPos.encode()
    new_ptxt_bytes = newPtxtAtPos.encode()

    with open(fctxt, 'rb') as f:
        data = bytearray(f.read())

    for i in range(len(ptxt_bytes)):
        data[pos + i] ^= ptxt_bytes[i] ^ new_ptxt_bytes[i]

    with open(fctxt + ".attck", 'wb') as f:
        f.write(data)


def main():
    if len(sys.argv) != 5:
        print("Usage: python chacha20_int_attck.py <fctxt> <pos> <ptxtAtPos> <newPtxtAtPos>")
        return

    attack(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    main()