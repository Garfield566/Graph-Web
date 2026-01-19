@echo off
title Generateur de Graphiques TikZ
cd /d "%~dp0"

echo ============================================================
echo   GENERATEUR DE GRAPHIQUES TIKZ
echo   Demarrage de l'application...
echo ============================================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verifier si les dependances sont installees
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dependances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Impossible d'installer les dependances.
        pause
        exit /b 1
    )
)

echo [OK] Lancement du serveur...
echo.
echo L'application va s'ouvrir dans votre navigateur.
echo Pour arreter, fermez cette fenetre ou appuyez sur Ctrl+C
echo.

python app\server.py

pause
