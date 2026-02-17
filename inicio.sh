#!/bin/bash
echo "[+] Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "[+] Instalando PyTorch CPU..."
pip install torch --index-url https://download.pytorch.org/whl/cpu

echo "[+] Instalando dependencias..."
pip install -r requirements.txt

echo "[+] Instalación completada"
