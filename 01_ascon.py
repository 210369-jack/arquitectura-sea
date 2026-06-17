#!/usr/bin/env python3
# ============================================================
# ASCON-128 - Criptografía Ligera (Estándar NIST)
# ============================================================

from ascon import ascon_encrypt, ascon_decrypt
import os
import time

def demo_ascon():
    print("=" * 60)
    print("ASCON-128 - Criptografía Ligera NIST")
    print("=" * 60)
    
    # Generar clave y nonce
    key = os.urandom(16)
    nonce = os.urandom(16)
    mensaje = b"Hola Smart City desde ASCON!" * 10
    
    # Medir tiempo de cifrado
    start = time.perf_counter()
    ciphertext, tag = ascon_encrypt(key, nonce, mensaje, variant="Ascon-128")
    encrypt_time = time.perf_counter() - start
    
    # Medir tiempo de descifrado
    start = time.perf_counter()
    plaintext = ascon_decrypt(key, nonce, ciphertext, tag, variant="Ascon-128")
    decrypt_time = time.perf_counter() - start
    
    print(f"Tamaño del mensaje: {len(mensaje)} bytes")
    print(f"Tiempo de cifrado: {encrypt_time*1000:.3f} ms")
    print(f"Tiempo de descifrado: {decrypt_time*1000:.3f} ms")
    print(f"✅ Éxito: {mensaje == plaintext}\n")
    
    return encrypt_time, decrypt_time

if __name__ == "__main__":
    demo_ascon()
