import sys, os
from multiprocessing import Process, Pipe

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import dh, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography import x509

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


def mkpair(x, y):
    """produz uma byte-string contendo o tuplo '(x,y)' ('x' e 'y' são byte-strings)"""
    len_x = len(x)
    len_x_bytes = len_x.to_bytes(2, "little")
    return len_x_bytes + x + y

def unpair(xy):
    """extrai componentes de um par codificado com 'mkpair'"""
    len_x = int.from_bytes(xy[:2], "little")
    x = xy[2 : len_x + 2]
    y = xy[len_x + 2 :]
    return x, y


def load_private_key(filename):
    with open(filename, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_cert(filename):
    with open(filename, "rb") as f:
        return x509.load_pem_x509_certificate(f.read())

def sign(priv_key, data):
    return priv_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def verify(pub_key, signature, data):
    pub_key.verify(
        signature, data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def verify_cert(cert, ca_cert):
    ca_cert.public_key().verify(
        cert.signature,
        cert.tbs_certificate_bytes,
        padding.PKCS1v15(),
        cert.signature_hash_algorithm
    )


def generate_parameters():
    return dh.DHParameterNumbers(p, g).parameters()

def derive_key(shared_key):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"sts key",
    )
    return hkdf.derive(shared_key)


def alice_process(conn):
    parameters = generate_parameters()

    priv = parameters.generate_private_key()
    pub = priv.public_key()

    alice_priv = load_private_key("Alice.key")
    alice_cert = load_cert("Alice.crt")
    ca_cert = load_cert("CA.crt")

    alice_bytes = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Enviar gx (chave pública de Alice)
    conn.send(alice_bytes)

    # Receber resposta de Bob: gy, assinatura e certificado de Bob
    msg = conn.recv()
    bob_bytes, rest = unpair(msg)
    sigB, certB_bytes = unpair(rest)

    bob_pub = serialization.load_pem_public_key(bob_bytes)
    certB = x509.load_pem_x509_certificate(certB_bytes)

    # Verificar certificado e assinatura
    verify_cert(certB, ca_cert)
    verify(certB.public_key(), sigB, bob_bytes + alice_bytes)

    print("Alice: valid signature from Bob")

    # Enviar assinatura e certificado de Alice
    signature = sign(alice_priv, alice_bytes + bob_bytes)

    msg = mkpair(signature, alice_cert.public_bytes(serialization.Encoding.PEM))
    conn.send(msg)

    # DH + AES-GCM
    shared = priv.exchange(bob_pub)
    key = derive_key(shared)
    print("Alice derived key:", key.hex())

    message = b"Hello Bob!"
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    ciphertext = aesgcm.encrypt(nonce, message, None)
    conn.send(nonce + ciphertext)


def bob_process(conn):
    parameters = generate_parameters()

    priv = parameters.generate_private_key()
    pub = priv.public_key()

    bob_priv = load_private_key("Bob.key")
    bob_cert = load_cert("Bob.crt")
    ca_cert = load_cert("CA.crt")

    # receber gx (chave pública de Alice)
    alice_bytes = conn.recv()
    alice_pub = serialization.load_pem_public_key(alice_bytes)

    # Gerar gy (chave pública de Bob)
    bob_bytes = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Assinar (gy || gx)
    signature = sign(bob_priv, bob_bytes + alice_bytes)

    # Enviar gy, assinatura e certificado de Bob
    msg = mkpair(bob_bytes, mkpair(signature, bob_cert.public_bytes(serialization.Encoding.PEM)))

    conn.send(msg)

    # Receber resposta de Alice: assinatura e certificado de Alice
    msg = conn.recv()
    sigA, certA_bytes = unpair(msg)
    certA = x509.load_pem_x509_certificate(certA_bytes)

    # Verificar certificado e assinatura
    verify_cert(certA, ca_cert)
    verify(certA.public_key(), sigA, alice_bytes + bob_bytes)

    print("Bob: valid signature from Alice")

    # DH + AES-GCM
    shared = priv.exchange(alice_pub)
    key = derive_key(shared)
    print("Bob key:", key.hex())

    # receber mensagem cifrada de Alice
    data = conn.recv()
    nonce = data[:12]
    ciphertext = data[12:]

    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    print("Bob received:", plaintext.decode())


def main():
    parent_conn, child_conn = Pipe()
    p1 = Process(target=alice_process, args=(parent_conn,))
    p2 = Process(target=bob_process, args=(child_conn,))
    p1.start(); p2.start()
    p1.join(); p2.join()


if __name__ == "__main__":
    main()