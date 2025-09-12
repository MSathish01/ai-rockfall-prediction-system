#!/usr/bin/env python3
"""
Main runner script for the AI-Based Rockfall Prediction System
"""

import os
import sys
import subprocess
import threading
import time
import signal
from pathlib import Path

class RockfallSystemRunner:
    def __init__(self):
        self.processes = []
        self.running = False
        
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        # Check Python dependencies
        try:
            import flask
            import numpy
            import pandas
            import sklearn
            print("✅ Python dependencies found")
        except ImportError as e:
            print(f"❌ Missing Python dependency: {e}")
            print("Run: pip install -r requirements.txt")
            return False
        
        # Check if frontend dependencies are installed
        if os.path.exists('frontend/node_modules'):
            print("✅ Frontend dependencies found")
        else:
            print("❌ Frontend dependencies not found")
            print("Run: cd frontend && npm install")
            return False
        
        return True
    
    def start_backend(self):
        """Start the Flask backend server"""
        print("🚀 Starting backend server...")
        
        # Set environment variables
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd()
        env['FLASK_ENV'] = 'development'
        
        # Start backend process
        backend_process = subprocess.Popen(
            [sys.executable, 'backend/app.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        self.processes.append(('backend', backend_process))
        print("✅ Backend server started on http://localhost:5000")
        
        return backend_process
    
    def start_frontend(self):
        """Start the React frontend server"""
        print("🚀 Starting frontend server...")
        
        # Change to frontend directory and start
        frontend_process = subprocess.Popen(
            ['npm', 'start'],
            cwd='frontend',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        self.processes.append(('frontend', frontend_process))
        print("✅ Frontend server started on http://localhost:3000")
        
        return frontend_process
    
    def start_sensor_simulator(self):
        """Start the sensor data simulator"""
        print("🚀 Starting sensor simulator...")
        
        simulator_process = subprocess.Popen(
            [sys.executable, 'data_processing/sensor_simulator.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        self.processes.append(('simulator', simulator_process))
        print("✅ Sensor simulator started")
        
        return simulator_process
    
    def monitor_processes(self):
        """Monitor all processes and restart if needed"""
        while self.running:
            for name, process in self.processes:
                if process.poll() is not None:
                    print(f"⚠️  Process {name} has stopped")
                    # In a production system, you might want to restart the process
            
            time.sleep(5)
    
    def stop_all_processes(self):
        """Stop all running processes"""
        print("\n🛑 Stopping all processes...")
        self.running = False
        
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Stopped {name}")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"🔥 Force killed {name}")
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
        
        self.processes.clear()
    
    def signal_handler(self, signum, frame):
        """Handle interrupt signals"""
        print(f"\n📡 Received signal {signum}")
        self.stop_all_processes()
        sys.exit(0)
    
    def run(self, start_simulator=False):
        """Run the complete system"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("🎯 AI-Based Rockfall Prediction System")
        print("=" * 50)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Create necessary directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('ml_models', exist_ok=True)
        
        self.running = True
        
        try:
            # Start backend
            self.start_backend()
            time.sleep(3)  # Wait for backend to start
            
            # Start frontend
            self.start_frontend()
            time.sleep(3)  # Wait for frontend to start
            
            # Start sensor simulator if requested
            if start_simulator:
                self.start_sensor_simulator()
            
            print("\n" + "=" * 50)
            print("🎉 System is running!")
            print("📊 Dashboard: http://localhost:3000")
            print("🔧 API: http://localhost:5000")
            print("📝 API Health: http://localhost:5000/api/health")
            print("\nPress Ctrl+C to stop all services")
            print("=" * 50)
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self.monitor_processes)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n📡 Received interrupt signal")
        except Exception as e:
            print(f"❌ Error running system: {e}")
        finally:
            self.stop_all_processes()
        
        return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run the AI-Based Rockfall Prediction System')
    parser.add_argument('--with-simulator', action='store_true', 
                       help='Start with sensor data simulator')
    parser.add_argument('--setup', action='store_true',
                       help='Run initial setup')
    
    args = parser.parse_args()
    
    if args.setup:
        print("🔧 Running initial setup...")
        setup_result = subprocess.run([sys.executable, 'scripts/setup.py'])
        if setup_result.returncode != 0:
            print("❌ Setup failed")
            return False
        print("✅ Setup completed")
    
    # Run the system
    runner = RockfallSystemRunner()
    return runner.run(start_simulator=args.with_simulator)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)