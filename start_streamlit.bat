@echo off
echo ====================================================
echo Starting CodeRescue AI Streamlit Web App...
echo ====================================================
cd /d "%~dp0coderescue-ai"
start "CodeRescue Streamlit App" cmd /k "streamlit run streamlit_app.py --server.port 8501"
echo.
echo CodeRescue AI Streamlit App starting!
echo Web App URL: http://localhost:8501
echo Video & Gallery URL: http://localhost:5000/media/
echo.
timeout /t 3 >nul
start http://localhost:8501
