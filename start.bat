@echo off
echo ====================================================
echo Starting CodeRescue Python Error Detector...
echo ====================================================
cd /d "%~dp0coderescue-ai"
start "CodeRescue Backend" cmd /k "node server.js"
cd client
start "CodeRescue Frontend" cmd /k "npm run dev"
echo.
echo Servers starting up!
echo Frontend URL: http://localhost:5173
echo Backend URL:  http://localhost:5000
echo.
timeout /t 3 >nul
start http://localhost:5173
