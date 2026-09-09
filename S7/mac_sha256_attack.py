import sys
import hashpumpy

def attack(fich, ext):

    with open(fich, "rb") as f:
        data = f.read()

    with open(fich + ".mac", "rb") as f:
        mac = f.read()

    mac_hex = mac.hex()
    key_len = 32

    new_mac, new_msg = hashpumpy.hashpump(
        mac_hex,
        data.decode(),
        ext,
        key_len
    )

    with open(fich + ".ext", "wb") as f:
        f.write(new_msg if isinstance(new_msg, bytes) else new_msg.encode())

    with open(fich + ".ext.mac", "wb") as f:
        f.write(bytes.fromhex(new_mac))


def main():

    if len(sys.argv) != 3:
        print("Usage: mac_sha256_attack.py <fich> <ext>")
        sys.exit(1)

    attack(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()