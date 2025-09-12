@echo off
echo Starting Rockfall Prediction System...
start "Backend" cmd /k "venv\Scripts\activate && python backend\app.py"
timeout /t 5
start "Frontend" cmd /k "cd frontend && npm start"
echo System started! Backend: http://localhost:5000, Frontend: http://localhost:3000
