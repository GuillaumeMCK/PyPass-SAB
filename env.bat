@echo off
title Python 3.11 (StartAllPatch ENV)
call env\Scripts\activate.bat
cls
echo You are on the python env for StartAllPatch, please dont toutch to libs please.
echo To leave the env, enter "deactivate"
echo.
echo Python Version:
Python\python.exe --version
echo.
cmd.exe
pause