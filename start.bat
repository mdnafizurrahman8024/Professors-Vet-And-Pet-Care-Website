@echo off
REM Double-click this file (or run: start.bat) to launch the local server.
REM It bypasses PowerShell's execution policy so it always works.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1" %*
pause
