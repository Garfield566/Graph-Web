@echo off
title Installation - Generateur de Graphiques TikZ
cd /d "%~dp0"

echo ============================================================
echo   INSTALLATION - GENERATEUR DE GRAPHIQUES TIKZ
echo ============================================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe.
    echo.
    echo Veuillez installer Python depuis:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Cochez "Add Python to PATH" lors de l'installation!
    echo.
    pause
    exit /b 1
)

echo [OK] Python detecte
python --version
echo.

REM Installer les dependances
echo [INFO] Installation des dependances Python...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Impossible d'installer les dependances.
    pause
    exit /b 1
)
echo [OK] Dependances installees
echo.

REM Creer le raccourci sur le bureau
echo [INFO] Creation du raccourci sur le bureau...

set SCRIPT_PATH=%~dp0run.bat
set SHORTCUT_NAME=Generateur Graphiques TikZ
set DESKTOP=%USERPROFILE%\Desktop

REM Utiliser PowerShell pour creer le raccourci
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\%SHORTCUT_NAME%.lnk'); $Shortcut.TargetPath = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'shell32.dll,21'; $Shortcut.Description = 'Generateur de Graphiques TikZ pour Obsidian'; $Shortcut.Save()"

if exist "%DESKTOP%\%SHORTCUT_NAME%.lnk" (
    echo [OK] Raccourci cree sur le bureau
) else (
    echo [ATTENTION] Le raccourci n'a pas pu etre cree automatiquement.
    echo Vous pouvez creer un raccourci manuellement vers: %SCRIPT_PATH%
)

echo.
echo ============================================================
echo   INSTALLATION TERMINEE !
echo ============================================================
echo.
echo Pour lancer l'application:
echo   1. Double-cliquez sur le raccourci "Generateur Graphiques TikZ" sur votre bureau
echo   OU
echo   2. Double-cliquez sur "run.bat" dans ce dossier
echo.
echo L'application s'ouvrira dans votre navigateur web.
echo.
pause
