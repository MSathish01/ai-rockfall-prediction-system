#!/usr/bin/env python3
"""
Setup script for the AI-Based Rockfall Prediction System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"✅ Node.js {result.stdout.strip()} detected")
        return True
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 16 or higher")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'ml_models',
        'data',
        'uploads',
        'exports'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

def setup_python_environment():
    """Set up Python virtual environment and install dependencies"""
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists('venv'):
        run_command('python -m venv venv', 'Creating virtual environment')
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
    else:  # Unix/Linux/macOS
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
    
    run_command(f'{pip_cmd} install --upgrade pip', 'Upgrading pip')
    run_command(f'{pip_cmd} install -r requirements.txt', 'Installing Python dependencies')

def setup_frontend():
    """Set up frontend dependencies"""
    if not check_node_version():
        return False
    
    os.chdir('frontend')
    run_command('npm install', 'Installing frontend dependencies')
    os.chdir('..')
    return True

def setup_database():
    """Initialize database"""
    print("🔄 Setting up database...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("📝 Created .env file from template")
        print("⚠️  Please update .env file with your configuration")
    
    # Initialize database tables
    init_script = """
import sys
sys.path.append('backend')
from app import app, db
with app.app_context():
    db.create_all()
    print("Database tables created successfully")
"""
    
    with open('temp_init_db.py', 'w') as f:
        f.write(init_script)
    
    if os.name == 'nt':
        python_cmd = 'venv\\Scripts\\python'
    else:
        python_cmd = 'venv/bin/python'
    
    run_command(f'{python_cmd} temp_init_db.py', 'Initializing database')
    os.remove('temp_init_db.py')

def setup_ml_models():
    """Initialize ML models"""
    print("🔄 Setting up ML models...")
    
    init_script = """
import sys
sys.path.append('ml_models')
from rockfall_predictor import RockfallPredictor
predictor = RockfallPredictor()
print("ML models initialized successfully")
"""
    
    with open('temp_init_ml.py', 'w') as f:
        f.write(init_script)
    
    if os.name == 'nt':
        python_cmd = 'venv\\Scripts\\python'
    else:
        python_cmd = 'venv/bin/python'
    
    run_command(f'{python_cmd} temp_init_ml.py', 'Initializing ML models')
    os.remove('temp_init_ml.py')

def create_startup_scripts():
    """Create startup scripts for easy deployment"""
    
    # Windows startup script
    windows_script = """@echo off
echo Starting Rockfall Prediction System...
start "Backend" cmd /k "venv\\Scripts\\activate && python backend\\app.py"
timeout /t 5
start "Frontend" cmd /k "cd frontend && npm start"
echo System started! Backend: http://localhost:5000, Frontend: http://localhost:3000
"""
    
    with open('start_windows.bat', 'w') as f:
        f.write(windows_script)
    
    # Unix/Linux startup script
    unix_script = """#!/bin/bash
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
"""
    
    with open('start_unix.sh', 'w') as f:
        f.write(unix_script)
    
    # Make Unix script executable
    if os.name != 'nt':
        os.chmod('start_unix.sh', 0o755)
    
    print("📝 Created startup scripts")

def main():
    """Main setup function"""
    print("🚀 Setting up AI-Based Rockfall Prediction System")
    print("=" * 50)
    
    # Check prerequisites
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Setup Python environment
    setup_python_environment()
    
    # Setup frontend
    if setup_frontend():
        print("✅ Frontend setup completed")
    else:
        print("⚠️  Frontend setup skipped (Node.js not available)")
    
    # Setup database
    setup_database()
    
    # Setup ML models
    setup_ml_models()
    
    # Create startup scripts
    create_startup_scripts()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update .env file with your configuration")
    print("2. Configure emergency contacts in config/emergency_contacts.json")
    print("3. Start the system:")
    if os.name == 'nt':
        print("   - Windows: run start_windows.bat")
    else:
        print("   - Unix/Linux: run ./start_unix.sh")
    print("4. Access the dashboard at http://localhost:3000")
    print("\nFor production deployment, use Docker:")
    print("   docker-compose -f deployment/docker-compose.yml up -d")

if __name__ == "__main__":
    main()