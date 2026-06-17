#!/usr/bin/env python3
# ============================================================
# ChaCha20-Poly1305 - Cifrado Ligero y Rápido
# ============================================================

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os
import time

def demo_chacha():
    print("=" * 60)
    print("ChaCha20-Poly1305 - Cifrado Rápido")
    print("=" * 60)
    
    key = ChaCha20Poly1305.generate_key()
    nonce = os.urandom(12)
    mensaje = b"Mensaje cifrado con ChaCha20-Poly1305" * 10
    
    # Cifrar
    start = time.perf_counter()
    cipher = ChaCha20Poly1305(key)
    ciphertext = cipher.encrypt(nonce, mensaje, None)
    encrypt_time = time.perf_counter() - start
    
    # Descifrar
    start = time.perf_counter()
    plaintext = cipher.decrypt(nonce, ciphertext, None)
    decrypt_time = time.perf_counter() - start
    
    print(f"Tamaño del mensaje: {len(mensaje)} bytes")
    print(f"Tiempo de cifrado: {encrypt_time*1000:.3f} ms")
    print(f"Tiempo de descifrado: {decrypt_time*1000:.3f} ms")
    print(f"✅ Éxito: {mensaje == plaintext}\n")
    
    return encrypt_time, decrypt_time

if __name__ == "__main__":
    demo_chacha()
