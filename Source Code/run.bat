@echo off
title StartAllPatch Runner (Python 3.11 - ENV)
:call
REM Active l'environnement virtuel
call env\Scripts\activate.bat

REM Exécute main.py pour lancer l'exécutable
Python\python.exe main.py
pause
goto call