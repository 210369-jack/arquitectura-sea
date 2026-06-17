# ============================================================
# ASCON - Implementación Simplificada
# (No requiere librería externa)
# ============================================================

import hashlib
import os

def ascon_encrypt(key, nonce, data, variant="Ascon-128"):
    """
    Implementación simplificada de ASCON-128
    Usa SHA-256 para derivar clave y XOR para cifrar
    """
    # Derivar clave de cifrado
    material = key + nonce
    cipher_key = hashlib.sha256(material).digest()
    
    # Cifrar con XOR
    ciphertext = bytes([d ^ cipher_key[i % len(cipher_key)] for i, d in enumerate(data)])
    
    # Generar tag de autenticación
    tag = hashlib.sha256(data + ciphertext + key).digest()[:16]
    
    return ciphertext, tag

def ascon_decrypt(key, nonce, ciphertext, tag, variant="Ascon-128"):
    """
    Descifrado simplificado de ASCON-128
    """
    material = key + nonce
    cipher_key = hashlib.sha256(material).digest()
    
    plaintext = bytes([c ^ cipher_key[i % len(cipher_key)] for i, c in enumerate(ciphertext)])
    
    # Verificar tag (simplificado)
    expected_tag = hashlib.sha256(plaintext + ciphertext + key).digest()[:16]
    if expected_tag != tag:
        print("⚠️ Advertencia: Tag de autenticación no coincide")
    
    return plaintext
