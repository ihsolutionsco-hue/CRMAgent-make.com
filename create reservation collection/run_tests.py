#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar los tests del mock server
Primero inicia el servidor mock, luego ejecuta los tests
"""

import subprocess
import sys
import time
import os
import signal

def run_tests():
    """Ejecuta el servidor mock y los tests"""
    print("=" * 80)
    print("EJECUTANDO TESTS DE CREATE RESERVATION")
    print("=" * 80)
    print()
    
    # Iniciar servidor mock en background
    print("[INFO] Iniciando servidor mock...")
    server_process = subprocess.Popen(
        [sys.executable, "mock_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Esperar a que el servidor esté listo
    print("[INFO] Esperando a que el servidor esté listo...")
    time.sleep(3)
    
    try:
        # Ejecutar tests
        print("[INFO] Ejecutando tests...")
        print()
        result = subprocess.run(
            [sys.executable, "test_create_reservation.py"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        return result.returncode == 0
    finally:
        # Cerrar servidor mock
        print()
        print("[INFO] Cerrando servidor mock...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)



