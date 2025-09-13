@echo off
echo 🚀 Starting AI-Based Rockfall Prediction System
echo ================================================

echo 🔧 Activating virtual environment...
call venv\Scripts\activate

echo 🔧 Starting Backend Server...
start "Rockfall Backend" cmd /k "venv\Scripts\activate && cd backend && python app.py"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo 🌐 Starting Frontend Dashboard...
start "Rockfall Frontend" cmd /k "cd frontend && npm start"

echo 📡 Starting Sensor Simulator...
start "Sensor Simulator" cmd /k "venv\Scripts\activate && python start_simulator.py"

echo.
echo ✅ System Started Successfully!
echo ================================================
echo 📊 Dashboard: http://localhost:3000
echo 🔧 API: http://localhost:5000
echo 📝 API Health: http://localhost:5000/api/health
echo.
echo 🎯 All services are starting in separate windows
echo 🔄 The sensor simulator will generate realistic data
echo 📈 Check the dashboard for real-time updates
echo.
echo Press any key to continue...
pause > nul