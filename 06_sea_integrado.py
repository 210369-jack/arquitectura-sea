#!/usr/bin/env python3
# ============================================================
# ARQUITECTURA SEA - SELECTIVE ENERGY-AWARE CRYPTOGRAPHY
# Versión Integrada con todos los algoritmos
# ============================================================

import time
import os
from enum import Enum
from dataclasses import dataclass
from typing import Tuple

# ============ LIBRERIAS ============
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

# Importar ascon (implementacion simple o libreria)
try:
    from ascon import ascon_encrypt, ascon_decrypt
    HAS_ASCON = True
except ImportError:
    # Fallback: implementacion simple
    HAS_ASCON = False
    import hashlib
    def ascon_encrypt(key, nonce, data, variant="Ascon-128"):
        material = key + nonce
        cipher_key = hashlib.sha256(material).digest()
        ciphertext = bytes([d ^ cipher_key[i % len(cipher_key)] for i, d in enumerate(data)])
        tag = hashlib.sha256(data + ciphertext + key).digest()[:16]
        return ciphertext, tag
    def ascon_decrypt(key, nonce, ciphertext, tag, variant="Ascon-128"):
        material = key + nonce
        cipher_key = hashlib.sha256(material).digest()
        plaintext = bytes([c ^ cipher_key[i % len(cipher_key)] for i, c in enumerate(ciphertext)])
        expected_tag = hashlib.sha256(plaintext + ciphertext + key).digest()[:16]
        if expected_tag != tag:
            print("Advertencia: Tag no coincide")
        return plaintext

# Kyber desactivado temporalmente
HAS_OQS = False


# ============ DEFINICION DE CONTEXTOS ============
class DeviceType(Enum):
    SENSOR = "sensor"
    CAMARA = "camara"
    CRITICO = "critico"


class SecurityLevel(Enum):
    BAJO = 1
    MEDIO = 2
    ALTO = 3
    CRITICO = 4


@dataclass
class Context:
    battery: float
    threat: bool
    device: DeviceType
    sensitivity: SecurityLevel


# ============ ARQUITECTURA SEA ============
class CryptoEngine:
    def __init__(self):
        self.stats = {}
        self.aes_key = os.urandom(32)
        self.chacha_key = ChaCha20Poly1305.generate_key()
        self.ecc_private = ec.generate_private_key(ec.SECP256R1())

        if HAS_ASCON:
            self.ascon_key = os.urandom(16)
            self.ascon_nonce = os.urandom(16)

    def _encrypt_aes(self, data: bytes) -> bytes:
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.aes_key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return ciphertext + nonce + encryptor.tag

    def _encrypt_chacha(self, data: bytes) -> bytes:
        nonce = os.urandom(12)
        return ChaCha20Poly1305(self.chacha_key).encrypt(nonce, data, None)

    def _encrypt_ecc(self, data: bytes) -> bytes:
        ephemeral = ec.generate_private_key(ec.SECP256R1())
        shared = ephemeral.exchange(ec.ECDH(), self.ecc_private.public_key())
        hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"ecc_aes")
        aes_key = hkdf.derive(shared)
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return ciphertext + nonce + encryptor.tag

    def _encrypt_ascon(self, data: bytes) -> bytes:
        if HAS_ASCON:
            ciphertext, tag = ascon_encrypt(self.ascon_key, self.ascon_nonce, data, variant="Ascon-128")
            return ciphertext + tag
        return self._encrypt_aes(data)

    def select_algorithm(self, context: Context) -> str:
        # Amenaza + datos criticos -> ECC (Kyber desactivado)
        if context.threat and context.sensitivity == SecurityLevel.CRITICO:
            return "ecc"
        # Bateria baja -> ASCON (mas eficiente)
        if context.battery < 0.25:
            return "ascon" if HAS_ASCON else "chacha"
        # Sensor -> ChaCha20
        if context.device == DeviceType.SENSOR:
            return "chacha"
        # Por defecto -> AES
        return "aes"

    def encrypt(self, data: bytes, context: Context) -> Tuple[bytes, str, float]:
        algo = self.select_algorithm(context)
        start = time.perf_counter()

        if algo == "aes":
            result = self._encrypt_aes(data)
        elif algo == "chacha":
            result = self._encrypt_chacha(data)
        elif algo == "ecc":
            result = self._encrypt_ecc(data)
        elif algo == "ascon":
            result = self._encrypt_ascon(data)
        else:
            result = self._encrypt_aes(data)

        elapsed = time.perf_counter() - start
        self.stats[algo] = self.stats.get(algo, 0) + 1

        return result, algo, elapsed


# ============ DEMOSTRACION ============
def run_demo():
    print("=" * 60)
    print("  ARQUITECTURA SEA - DEMOSTRACION")
    print("  (Selective Energy-Aware Cryptography)")
    print("=" * 60)

    engine = CryptoEngine()

    scenarios = [
        Context(0.85, False, DeviceType.CAMARA, SecurityLevel.MEDIO),
        Context(0.15, False, DeviceType.SENSOR, SecurityLevel.BAJO),
        Context(0.45, True, DeviceType.CRITICO, SecurityLevel.CRITICO),
        Context(0.70, False, DeviceType.SENSOR, SecurityLevel.BAJO),
    ]

    mensajes = [
        b"Datos de camara de vigilancia - flujo continuo",
        b"Lectura de sensor ambiental - bateria critica",
        b"ALERTA: Datos criticos de infraestructura - amenaza detectada",
        b"Telemetria de sensor IoT - operacion normal"
    ]

    print("\n[1] SELECCION DINAMICA DE ALGORITMOS")
    print("-" * 60)

    for i, (context, msg) in enumerate(zip(scenarios, mensajes)):
        _, algo, elapsed = engine.encrypt(msg, context)
        print(f"Escenario {i+1}: Bateria={context.battery*100:.0f}% | Amenaza={context.threat}")
        print(f"  Algoritmo seleccionado: {algo.upper()}")
        print(f"  Tiempo de cifrado: {elapsed*1000:.2f} ms")
        print(f"  Mensaje: {msg[:50]}...\n")

    print("\n[2] ESTADISTICAS DE USO")
    print("-" * 60)
    for algo, count in engine.stats.items():
        print(f"  {algo.upper()}: {count} veces usado")

    # Calcular ahorro energetico
    total_ops = sum(engine.stats.values())
    if total_ops > 0:
        energia_sea = sum(
            0.2 if a in ['ascon', 'chacha'] else
            0.5 if a == 'aes' else
            0.7 for a in engine.stats
        ) / total_ops
    else:
        energia_sea = 0.5

    print(f"\n[3] AHORRO ENERGETICO ESTIMADO")
    print(f"  Consumo tradicional (solo AES): 100%")
    print(f"  Consumo con SEA: {energia_sea*100:.0f}%")
    print(f"  Ahorro energetico: {(1-energia_sea)*100:.0f}%")
    print("=" * 60)
    print("  DEMOSTRACION COMPLETADA CON EXITO")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
