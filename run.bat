@echo off
echo ========================================
echo   QwenLM Mobile Bot
echo ========================================
echo.

REM Verificar si el entorno virtual existe
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] El entorno virtual no existe.
    echo Ejecuta: python -m venv .venv
    echo Luego: .venv\Scripts\activate && pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activar entorno virtual
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Verificar dependencias
echo Verificando dependencias...
pip install -q -r requirements.txt

REM Iniciar bot
echo.
echo Iniciando bot...
echo ========================================
echo.
python main.py

pause
