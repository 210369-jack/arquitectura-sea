#!/usr/bin/env python3
# ============================================================
# ECC - Curvas Elípticas (Intercambio de Claves)
# ============================================================

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import time

def demo_ecc():
    print("=" * 60)
    print("ECC (P-256) - Criptografía Asimétrica")
    print("=" * 60)
    
    # Generar claves
    start = time.perf_counter()
    private_key = ec.generate_private_key(ec.SECP256R1())
    receiver_private = ec.generate_private_key(ec.SECP256R1())
    
    # Intercambio ECDH
    shared_secret = private_key.exchange(ec.ECDH(), receiver_private.public_key())
    
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"ecc_key")
    aes_key = hkdf.derive(shared_secret)
    keygen_time = time.perf_counter() - start
    
    # Cifrar con AES
    nonce = os.urandom(12)
    mensaje = b"Mensaje cifrado con ECC + AES" * 10
    
    start = time.perf_counter()
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(mensaje) + encryptor.finalize()
    encrypt_time = time.perf_counter() - start
    
    print(f"Tamaño del mensaje: {len(mensaje)} bytes")
    print(f"Tiempo de generación de claves: {keygen_time*1000:.3f} ms")
    print(f"Tiempo de cifrado: {encrypt_time*1000:.3f} ms")
    print(f"✅ Cifrado completado\n")
    
    return keygen_time, encrypt_time

if __name__ == "__main__":
    demo_ecc()
