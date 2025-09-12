#!/bin/bash
echo "Starting Rockfall Prediction System..."
source venv/bin/activate
python backend/app.py &
BACKEND_PID=$!
cd frontend
npm start &
FRONTEND_PID=$!
echo "System started! Backend PID: $BACKEND_PID, Frontend PID: $FRONTEND_PID"
echo "Backend: http://localhost:5000, Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop all services"
wait
