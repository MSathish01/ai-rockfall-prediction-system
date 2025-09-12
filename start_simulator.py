#!/usr/bin/env python3
"""
Quick start script for the sensor simulator
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'data_processing'))

from sensor_simulator import SensorSimulator
import time
import threading

def run_simulator():
    """Run the sensor simulator"""
    simulator = SensorSimulator()
    
    print("🚀 Starting Rockfall Sensor Simulator...")
    print("📊 Generating realistic sensor data...")
    
    try:
        # Start continuous simulation
        threads = simulator.start_simulation()
        print("✅ Sensor simulation started successfully!")
        print("📡 Sending data to backend API...")
        print("⏹️  Press Ctrl+C to stop")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping sensor simulation...")
        simulator.stop_simulation()
        print("✅ Sensor simulation stopped")

if __name__ == "__main__":
    run_simulator()