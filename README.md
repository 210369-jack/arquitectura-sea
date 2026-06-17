# Arquitectura SEA - Selective Energy-Aware Cryptography

## 📋 Descripción
Arquitectura de criptografía adaptativa y verde para Smart Cities, con selección dinámica de algoritmos según contexto energético, sensibilidad de datos y tipo de dispositivo.

## 🚀 Algoritmos Implementados
- **ASCON-128**: Estándar NIST para criptografía ligera en IoT
- **AES-256-GCM**: Cifrado autenticado estándar de la industria
- **ECC (P-256)**: Criptografía asimétrica con curvas elípticas
- **ChaCha20-Poly1305**: Cifrado rápido y ligero

## 📊 Resultados de Experimentación
| Algoritmo | Tiempo Cifrado (ms) | Consumo Relativo |
|-----------|-------------------|------------------|
| ASCON-128 | 0.033 | 0.15 |
| AES-256-GCM | 5.927 | 0.50 |
| ECC P-256 | 0.176 | 0.40 |
| ChaCha20 | 0.088 | 0.30 |
| **SEA (promedio)** | **0.60** | **0.38** |

**Ahorro energético: 62%** 🎉

## 📦 Instalación
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
