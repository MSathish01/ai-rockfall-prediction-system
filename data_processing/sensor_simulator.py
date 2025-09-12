import requests
import json
import time
import random
import numpy as np
from datetime import datetime, timedelta
import threading

class SensorSimulator:
    def __init__(self, api_base_url="http://localhost:5000"):
        self.api_base_url = api_base_url
        self.sensors = self.initialize_sensors()
        self.running = False
        
    def initialize_sensors(self):
        """Initialize sensor configurations"""
        sensors = [
            {
                'sensor_id': 'DS-001',
                'sensor_type': 'displacement',
                'location_x': -23.5505,
                'location_y': -46.6333,
                'unit': 'mm',
                'base_value': 0.5,
                'noise_level': 0.1
            },
            {
                'sensor_id': 'SG-002',
                'sensor_type': 'strain',
                'location_x': -23.5515,
                'location_y': -46.6343,
                'unit': 'microstrain',
                'base_value': 100,
                'noise_level': 20
            },
            {
                'sensor_id': 'PP-003',
                'sensor_type': 'pore_pressure',
                'location_x': -23.5525,
                'location_y': -46.6353,
                'unit': 'kPa',
                'base_value': 50,
                'noise_level': 10
            },
            {
                'sensor_id': 'TM-004',
                'sensor_type': 'temperature',
                'location_x': -23.5535,
                'location_y': -46.6363,
                'unit': 'celsius',
                'base_value': 15,
                'noise_level': 5
            },
            {
                'sensor_id': 'RG-005',
                'sensor_type': 'rainfall',
                'location_x': -23.5545,
                'location_y': -46.6373,
                'unit': 'mm/h',
                'base_value': 2,
                'noise_level': 1
            },
            {
                'sensor_id': 'VM-006',
                'sensor_type': 'vibration',
                'location_x': -23.5555,
                'location_y': -46.6383,
                'unit': 'm/s2',
                'base_value': 0.05,
                'noise_level': 0.02
            }
        ]
        return sensors
    
    def generate_sensor_reading(self, sensor):
        """Generate realistic sensor reading with trends and noise"""
        # Add time-based trends
        hour = datetime.now().hour
        
        # Base value with daily patterns
        if sensor['sensor_type'] == 'temperature':
            # Temperature varies with time of day
            daily_variation = 10 * np.sin(2 * np.pi * hour / 24)
            base_value = sensor['base_value'] + daily_variation
        elif sensor['sensor_type'] == 'rainfall':
            # Rainfall has random spikes
            if random.random() < 0.1:  # 10% chance of rain
                base_value = sensor['base_value'] + random.exponential(5)
            else:
                base_value = 0
        else:
            base_value = sensor['base_value']
        
        # Add gradual trend (simulating geological changes)
        trend = random.uniform(-0.01, 0.02) * sensor['base_value']
        
        # Add noise
        noise = random.gauss(0, sensor['noise_level'])
        
        # Calculate final value
        value = max(0, base_value + trend + noise)
        
        # Add occasional spikes for critical sensors
        if sensor['sensor_type'] in ['displacement', 'strain'] and random.random() < 0.05:
            value *= random.uniform(1.5, 3.0)  # 5% chance of spike
        
        return round(value, 3)
    
    def send_sensor_data(self, sensor_data):
        """Send sensor data to the API"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/sensor-data",
                json=sensor_data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                print(f"✓ Sent data from {sensor_data['sensor_id']}: {sensor_data['value']} {sensor_data['unit']}")
            else:
                print(f"✗ Failed to send data from {sensor_data['sensor_id']}: {response.status_code}")
        except Exception as e:
            print(f"✗ Error sending data from {sensor_data['sensor_id']}: {e}")
    
    def simulate_sensor(self, sensor):
        """Simulate a single sensor continuously"""
        while self.running:
            try:
                value = self.generate_sensor_reading(sensor)
                
                sensor_data = {
                    'sensor_id': sensor['sensor_id'],
                    'sensor_type': sensor['sensor_type'],
                    'location_x': sensor['location_x'],
                    'location_y': sensor['location_y'],
                    'value': value,
                    'unit': sensor['unit'],
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                self.send_sensor_data(sensor_data)
                
                # Wait between readings (30-60 seconds)
                time.sleep(random.uniform(30, 60))
                
            except Exception as e:
                print(f"Error in sensor {sensor['sensor_id']}: {e}")
                time.sleep(60)  # Wait before retrying
    
    def start_simulation(self):
        """Start simulating all sensors"""
        print("Starting sensor simulation...")
        self.running = True
        
        # Start a thread for each sensor
        threads = []
        for sensor in self.sensors:
            thread = threading.Thread(target=self.simulate_sensor, args=(sensor,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            print(f"Started simulation for sensor {sensor['sensor_id']}")
        
        return threads
    
    def stop_simulation(self):
        """Stop sensor simulation"""
        print("Stopping sensor simulation...")
        self.running = False
    
    def simulate_emergency_scenario(self):
        """Simulate an emergency scenario with high risk readings"""
        print("🚨 Simulating emergency scenario...")
        
        emergency_data = [
            {
                'sensor_id': 'DS-001',
                'sensor_type': 'displacement',
                'location_x': -23.5505,
                'location_y': -46.6333,
                'value': 2.5,  # High displacement
                'unit': 'mm',
                'timestamp': datetime.utcnow().isoformat()
            },
            {
                'sensor_id': 'SG-002',
                'sensor_type': 'strain',
                'location_x': -23.5515,
                'location_y': -46.6343,
                'value': 200,  # High strain
                'unit': 'microstrain',
                'timestamp': datetime.utcnow().isoformat()
            },
            {
                'sensor_id': 'RG-005',
                'sensor_type': 'rainfall',
                'location_x': -23.5545,
                'location_y': -46.6373,
                'value': 15,  # Heavy rainfall
                'unit': 'mm/h',
                'timestamp': datetime.utcnow().isoformat()
            }
        ]
        
        for data in emergency_data:
            self.send_sensor_data(data)
            time.sleep(2)
    
    def generate_historical_data(self, days=30):
        """Generate historical data for training"""
        print(f"Generating {days} days of historical data...")
        
        start_date = datetime.utcnow() - timedelta(days=days)
        current_date = start_date
        
        while current_date < datetime.utcnow():
            for sensor in self.sensors:
                # Generate multiple readings per day
                for _ in range(random.randint(20, 50)):
                    reading_time = current_date + timedelta(
                        hours=random.uniform(0, 24),
                        minutes=random.uniform(0, 60)
                    )
                    
                    if reading_time > datetime.utcnow():
                        break
                    
                    # Temporarily modify sensor for historical context
                    temp_sensor = sensor.copy()
                    temp_sensor['timestamp'] = reading_time
                    
                    value = self.generate_sensor_reading(temp_sensor)
                    
                    sensor_data = {
                        'sensor_id': sensor['sensor_id'],
                        'sensor_type': sensor['sensor_type'],
                        'location_x': sensor['location_x'],
                        'location_y': sensor['location_y'],
                        'value': value,
                        'unit': sensor['unit'],
                        'timestamp': reading_time.isoformat()
                    }
                    
                    self.send_sensor_data(sensor_data)
                    time.sleep(0.1)  # Small delay to avoid overwhelming the API
            
            current_date += timedelta(days=1)
            print(f"Generated data for {current_date.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    simulator = SensorSimulator()
    
    print("Rockfall Sensor Simulator")
    print("1. Start continuous simulation")
    print("2. Generate historical data")
    print("3. Simulate emergency scenario")
    print("4. Exit")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        try:
            threads = simulator.start_simulation()
            print("Simulation running... Press Ctrl+C to stop")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            simulator.stop_simulation()
            print("\nSimulation stopped")
    
    elif choice == "2":
        days = int(input("Enter number of days of historical data to generate (default 7): ") or 7)
        simulator.generate_historical_data(days)
        print("Historical data generation completed")
    
    elif choice == "3":
        simulator.simulate_emergency_scenario()
        print("Emergency scenario simulation completed")
    
    else:
        print("Exiting...")