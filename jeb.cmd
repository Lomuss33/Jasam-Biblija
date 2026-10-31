@echo off
setlocal
if not exist "%~dp0.venv\Scripts\python.exe" goto missing_venv
"%~dp0.venv\Scripts\python.exe" -m jeb --root "%~dp0." work %*
exit /b %ERRORLEVEL%
:missing_venv
echo This repository needs its local Python 3.13 environment.
echo Run the three setup commands in README.md, then run .\jeb.cmd again.
exit /b 2
