@echo off
chcp 65001 >nul
echo ========================================================================
echo EJECUTANDO TESTS DE CREATE RESERVATION
echo ========================================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar si las dependencias están instaladas
echo [INFO] Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo.
echo [INFO] Ejecutando tests...
echo.

python run_tests.py

if errorlevel 1 (
    echo.
    echo [ERROR] Los tests fallaron
    pause
    exit /b 1
) else (
    echo.
    echo [OK] Tests completados exitosamente
    pause
)



