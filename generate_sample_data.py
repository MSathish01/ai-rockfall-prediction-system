#!/usr/bin/env python3
"""
Generate sample data for the rockfall prediction system
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate and send sample sensor data to populate the dashboard"""
    
    base_url = "http://localhost:5000"
    
    # Sample sensor configurations
    sensors = [
        {
            'sensor_id': 'DS-001',
            'sensor_type': 'displacement',
            'location_x': -23.5505,
            'location_y': -46.6333,
            'unit': 'mm',
            'base_value': 0.5
        },
        {
            'sensor_id': 'SG-002', 
            'sensor_type': 'strain',
            'location_x': -23.5515,
            'location_y': -46.6343,
            'unit': 'microstrain',
            'base_value': 100
        },
        {
            'sensor_id': 'PP-003',
            'sensor_type': 'pore_pressure', 
            'location_x': -23.5525,
            'location_y': -46.6353,
            'unit': 'kPa',
            'base_value': 50
        },
        {
            'sensor_id': 'TM-004',
            'sensor_type': 'temperature',
            'location_x': -23.5535,
            'location_y': -46.6363,
            'unit': 'celsius',
            'base_value': 15
        },
        {
            'sensor_id': 'RG-005',
            'sensor_type': 'rainfall',
            'location_x': -23.5545,
            'location_y': -46.6373,
            'unit': 'mm/h',
            'base_value': 2
        }
    ]
    
    print("🚀 Generating sample data for dashboard...")
    
    # Generate 50 data points to populate the system
    for i in range(50):
        for sensor in sensors:
            # Generate realistic values with some variation
            if sensor['sensor_type'] == 'displacement':
                value = sensor['base_value'] + random.uniform(-0.2, 0.8)
                if random.random() < 0.1:  # 10% chance of high reading
                    value += random.uniform(1.0, 2.0)
            elif sensor['sensor_type'] == 'strain':
                value = sensor['base_value'] + random.uniform(-30, 80)
                if random.random() < 0.1:  # 10% chance of high reading
                    value += random.uniform(50, 150)
            elif sensor['sensor_type'] == 'pore_pressure':
                value = sensor['base_value'] + random.uniform(-15, 25)
            elif sensor['sensor_type'] == 'temperature':
                value = sensor['base_value'] + random.uniform(-5, 10)
            elif sensor['sensor_type'] == 'rainfall':
                if random.random() < 0.3:  # 30% chance of rain
                    value = random.uniform(0, 15)
                else:
                    value = 0
            else:
                value = sensor['base_value'] + random.uniform(-0.1, 0.1)
            
            # Create timestamp (spread over last 2 hours)
            timestamp = datetime.utcnow() - timedelta(minutes=random.randint(0, 120))
            
            sensor_data = {
                'sensor_id': sensor['sensor_id'],
                'sensor_type': sensor['sensor_type'],
                'location_x': sensor['location_x'],
                'location_y': sensor['location_y'],
                'value': round(max(0, value), 3),
                'unit': sensor['unit'],
                'timestamp': timestamp.isoformat() + 'Z'
            }
            
            try:
                response = requests.post(
                    f"{base_url}/api/sensor-data",
                    json=sensor_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"✅ Sent {sensor['sensor_id']}: {value:.2f} {sensor['unit']}")
                else:
                    print(f"❌ Failed to send {sensor['sensor_id']}: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Error sending data for {sensor['sensor_id']}: {e}")
            
            # Small delay between requests
            time.sleep(0.1)
        
        # Delay between sensor cycles
        time.sleep(0.5)
    
    print("\n✅ Sample data generation completed!")
    print("📊 Dashboard should now show meaningful data")
    print("🔄 Refresh your browser to see the updated information")

if __name__ == "__main__":
    try:
        generate_sample_data()
    except KeyboardInterrupt:
        print("\n🛑 Data generation stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the backend server is running on http://localhost:5000")