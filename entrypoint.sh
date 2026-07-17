#!/bin/bash
set -e

echo "Esperando base de datos..."
sleep 5

echo "Inicializando base de datos y semillas..."
python init_and_seed.py

echo "Iniciando servidor..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload