@echo off
title SAPUpdaterD - Builder

:: Ask the user for the project path
set /p "projectPath=Enter the full path to StartAllPatch UpdaterD: "

:: Build the project using dotnet publish with self-contained deployment
cd "%projectPath%"
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true -o "%projectPath%\build"

:: Notify the user of completion
echo Build completed. The self-contained output files are located in %projectPath%\build.
pause
