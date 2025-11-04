#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar el servidor mock y los tests automáticamente
"""

import subprocess
import sys
import time
import requests
import os
import io

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def wait_for_server(url, max_attempts=10, delay=1):
    """Espera a que el servidor esté disponible"""
    for i in range(max_attempts):
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                print(f"[OK] Servidor mock esta corriendo en {url}")
                return True
        except:
            pass
        time.sleep(delay)
        print(f"Esperando servidor... ({i+1}/{max_attempts})")
    return False

def main():
    print("=" * 80)
    print("INICIANDO SERVERS Y TESTS")
    print("=" * 80)
    
    # Iniciar servidor mock
    print("\n[1/2] Iniciando servidor mock...")
    server_process = subprocess.Popen(
        [sys.executable, "mock_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Esperar a que el servidor esté listo
    server_url = "http://localhost:5000"
    if not wait_for_server(server_url):
        print("[ERROR] No se pudo iniciar el servidor mock")
        print("Stderr:", server_process.stderr.read() if server_process.stderr else "N/A")
        server_process.terminate()
        return 1
    
    # Ejecutar tests
    print("\n[2/2] Ejecutando tests...")
    print("=" * 80)
    
    try:
        result = subprocess.run(
            [sys.executable, "test_create_contact.py"],
            cwd=os.getcwd(),
            text=True
        )
        return_code = result.returncode
    except Exception as e:
        print(f"[ERROR] Error ejecutando tests: {e}")
        return_code = 1
    finally:
        # Terminar servidor
        print("\n" + "=" * 80)
        print("Deteniendo servidor mock...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("[OK] Servidor detenido")
    
    return return_code

if __name__ == "__main__":
    sys.exit(main())

