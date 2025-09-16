@echo off
echo Starting AI Rockfall Prediction System...

echo Starting Backend Server...
start "Rockfall Backend" cmd /k "cd /d C:\Users\msath\OneDrive\Desktop\Kiro && .\venv\Scripts\activate && python backend\app.py"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo Starting Frontend Server...
start "Rockfall Frontend" cmd /k "cd /d C:\Users\msath\OneDrive\Desktop\Kiro\frontend && npm start"

echo.
echo ✅ System Starting!
echo.
echo Backend will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:3000
echo.
echo Both services will open in separate windows.
echo Close those windows to stop the services.
echo.
pause