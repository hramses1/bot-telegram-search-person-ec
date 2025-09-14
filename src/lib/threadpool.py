# src/lib/threadpool.py
from concurrent.futures import ThreadPoolExecutor

# Ajusta según tu servidor/CPU y la carga de tu API
EXECUTOR = ThreadPoolExecutor(max_workers=8)
