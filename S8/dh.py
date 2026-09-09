import sys
from multiprocessing import Process, Pipe

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

p = int("""
    FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B
    80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22
    514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D
    F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6
    F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB
    5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
    C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8
    FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB
    9ED52907 7096966D 670C354E 4ABC9804 F1746C08
    CA18217C 32905E46 2E36CE3B E39E772C 180E8603
    9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6
    95581718 3995497C EA956AE5 15D22618 98FA0510
    15728E5A 8AACAA68 FFFFFFFF FFFFFFFF""".replace(" ", "").replace("\n", ""), 16)

g = 2


def generate_parameters():
    return dh.DHParameterNumbers(p, g).parameters()

def alice_process(conn):
    parameters = generate_parameters()

    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()

    alice_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    conn.send(alice_bytes)

    bob_bytes = conn.recv()
    bob_public_key = serialization.load_pem_public_key(bob_bytes)

    shared_key = private_key.exchange(bob_public_key)

    print("Alice key:", shared_key.hex())

def bob_process(conn):
    parameters = generate_parameters()

    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()

    alice_bytes = conn.recv()
    alice_public_key = serialization.load_pem_public_key(alice_bytes)

    bob_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    conn.send(bob_bytes)

    shared_key = private_key.exchange(alice_public_key)

    print("Bob key:", shared_key.hex())

def main():
    parent_conn, child_conn = Pipe()
    p1 = Process(target=alice_process, args=(parent_conn,))
    p2 = Process(target=bob_process, args=(child_conn,))
    p1.start(); p2.start()
    p1.join(); p2.join()


if __name__ == "__main__":
    main()