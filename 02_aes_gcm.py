#!/usr/bin/env python3
# ============================================================
# AES-256-GCM - Cifrado Simétrico Autenticado
# ============================================================

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time

def demo_aes_gcm():
    print("=" * 60)
    print("AES-256-GCM - Cifrado Estándar")
    print("=" * 60)
    
    key = os.urandom(32)
    nonce = os.urandom(12)
    mensaje = b"Mensaje cifrado con AES-256-GCM" * 10
    
    # Cifrar
    start = time.perf_counter()
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(mensaje) + encryptor.finalize()
    tag = encryptor.tag
    encrypt_time = time.perf_counter() - start
    
    # Descifrar
    start = time.perf_counter()
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    decrypt_time = time.perf_counter() - start
    
    print(f"Tamaño del mensaje: {len(mensaje)} bytes")
    print(f"Tiempo de cifrado: {encrypt_time*1000:.3f} ms")
    print(f"Tiempo de descifrado: {decrypt_time*1000:.3f} ms")
    print(f"✅ Éxito: {mensaje == plaintext}\n")
    
    return encrypt_time, decrypt_time

if __name__ == "__main__":
    demo_aes_gcm()
