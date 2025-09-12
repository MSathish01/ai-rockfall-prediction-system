@echo off
echo 🚀 Starting AI-Based Rockfall Prediction System
echo ================================================

echo 🔧 Starting Backend Server...
start "Backend" cmd /k "cd backend && python app.py"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo 🌐 Starting Frontend Dashboard...
start "Frontend" cmd /k "cd frontend && npm start"

echo ⏳ Waiting for frontend to start...
timeout /t 3 /nobreak > nul

echo ✅ System Started Successfully!
echo 📊 Dashboard: http://localhost:3000
echo 🔧 API: http://localhost:5000
echo.
echo Press any key to continue...
pause > nul