#!/usr/bin/env python3
# ============================================================
# SCRIPT PARA EJECUTAR TODOS LOS EXPERIMENTOS
# ============================================================

import subprocess
import time
import os

print("=" * 70)
print("  EJECUTANDO TODOS LOS EXPERIMENTOS DE LA ARQUITECTURA SEA")
print("=" * 70)

# Los archivos están en la misma carpeta (raíz)
experimentos = [
    ("01_ascon.py", "ASCON-128"),
    ("02_aes_gcm.py", "AES-256-GCM"),
    ("03_ecc.py", "ECC P-256"),
    ("05_chacha.py", "ChaCha20-Poly1305"),
    ("06_sea_integrado.py", "SEA Integrado"),
    ("07_sea_optimizado.py", "SEA Optimizado"),
]

resultados = []

for archivo, nombre in experimentos:
    print(f"\n>>> EJECUTANDO: {nombre} ({archivo})")
    print("-" * 70)

    try:
        start = time.perf_counter()
        resultado = subprocess.run(
            ["python3", archivo],
            capture_output=True,
            text=True,
            timeout=60
        )
        elapsed = time.perf_counter() - start

        if resultado.returncode == 0:
            print(resultado.stdout)
            resultados.append(f"✅ {nombre}: COMPLETADO ({elapsed:.2f}s)")
        else:
            print(f"❌ Error en {nombre}:")
            print(resultado.stderr)
            resultados.append(f"❌ {nombre}: ERROR")

    except subprocess.TimeoutExpired:
        print(f"❌ {nombre}: TIMEOUT")
        resultados.append(f"❌ {nombre}: TIMEOUT")
    except Exception as e:
        print(f"❌ {nombre}: {e}")
        resultados.append(f"❌ {nombre}: {e}")

print("\n" + "=" * 70)
print("  RESUMEN DE RESULTADOS")
print("=" * 70)

for r in resultados:
    print(f"  {r}")

print("=" * 70)
print("  EXPERIMENTOS COMPLETADOS")
print("=" * 70)
