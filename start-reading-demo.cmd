@echo off
setlocal
cd /d "%~dp0"
echo JSB - synthetic reading practice with private notes
echo This opens the invented examples, not an actual Bible text.
echo Leave this window open while reading. Stop with Ctrl+C.
echo.
where node >nul 2>nul
if errorlevel 1 goto missing_node
if not exist ".venv\Scripts\python.exe" goto missing_python
node web\reading-dev.mjs --synthetic
set "JEB_READING_LAUNCH_EXIT=%ERRORLEVEL%"
if "%JEB_READING_LAUNCH_EXIT%"=="0" exit /b 0
echo.
echo The reading desk could not start. Existing notes have been preserved.
echo See docs\READING_DESK_FIRST_SESSION.md and the error above.
pause
exit /b %JEB_READING_LAUNCH_EXIT%
:missing_node
echo Node.js 22 or later is needed. See README.md for the local viewer setup.
pause
exit /b 2
:missing_python
echo The local Python environment is missing. Follow the setup in README.md.
pause
exit /b 2
