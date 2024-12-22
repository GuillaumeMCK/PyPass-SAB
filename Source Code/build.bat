@echo off
title StartAllPatch Builder (Python 3.11 - ENV)
REM Active l'environnement virtuel
call env\Scripts\activate.bat

REM Exécute PyInstaller pour créer un fichier exécutable
pyinstaller --noconfirm --onefile --windowed --icon "D:\Software\PyCharm Project\StartAllPatch\src\assets\icon.ico" --uac-admin ^
--add-data "D:\Software\PyCharm Project\StartAllPatch\src\assets;assets/" ^
--add-data "D:\Software\PyCharm Project\StartAllPatch\env\Lib\site-packages\customtkinter;customtkinter/" ^
"D:\Software\PyCharm Project\StartAllPatch\main.py"

move dist\main.exe build\StartAllPatch\StartAllPatch.exe >nul

timeout 1 >nul
setlocal enabledelayedexpansion

:: Texte à afficher avant le chargement
set "text=Building"

:: Définir les caractères à afficher
set "spinner=\|/-"

:: Nombre de cycles du spinner avant l'arrêt
set max_cycles=10
set cycle=0

:loop
for /L %%i in (0,1,3) do (
    set "char=!spinner:~%%i,1!"
    <nul set /p "=!text! !char!"  :: Affiche le texte et le caractère sans sauter de ligne
    timeout /t 0 >nul
    cls
    <nul set /p "="     :: Efface l'affichage précédent (10 caractères)
    
    :: Incrémente le compteur de cycles
    set /a cycle+=1
    if !cycle! geq %max_cycles% goto end
)

goto loop

:end
echo The builded files is in "build\StartAllPatch"
echo Process Executed !
echo.
REM Met le script en pause pour voir les éventuelles erreurs
pause
