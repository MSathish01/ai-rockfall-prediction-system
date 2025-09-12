from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import sys
import json
import numpy as np
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///rockfall_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy()
db.init_app(app)

# Database Models (inline for simplicity)
class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)
    location_x = db.Column(db.Float, nullable=False)
    location_y = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    risk_level = db.Column(db.String(20), nullable=False)
    probability = db.Column(db.Float, nullable=False)
    affected_zones = db.Column(db.Text, nullable=False)
    recommendations = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='ACTIVE')

# Simple ML Predictor (inline)
class SimpleRockfallPredictor:
    def predict_rockfall_risk(self, sensor_data=None):
        # Generate mock prediction
        probability = random.uniform(0.2, 0.8)
        
        if probability < 0.3:
            risk_level = 'LOW'
        elif probability < 0.5:
            risk_level = 'MEDIUM'
        elif probability < 0.7:
            risk_level = 'HIGH'
        else:
            risk_level = 'CRITICAL'
        
        affected_zones = [
            {'lat': -23.5505, 'lng': -46.6333, 'radius': 50, 'risk_level': int(probability * 10)},
            {'lat': -23.5515, 'lng': -46.6343, 'radius': 75, 'risk_level': int(probability * 8)}
        ]
        
        recommendations = [
            f"Current risk level: {risk_level}",
            "Monitor conditions closely",
            "Follow safety protocols"
        ]
        
        if risk_level in ['HIGH', 'CRITICAL']:
            recommendations.extend([
                "Consider restricting access to high-risk areas",
                "Increase monitoring frequency"
            ])
        
        return {
            'risk_level': risk_level,
            'probability': probability,
            'affected_zones': affected_zones,
            'recommendations': recommendations,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def generate_risk_map(self, sensor_data_list):
        risk_zones = []
        for i in range(8):
            lat = -23.5505 + (i * 0.001)
            lng = -46.6333 + (i * 0.001)
            risk_value = random.uniform(0, 1)
            
            risk_zones.append({
                'lat': lat,
                'lng': lng,
                'risk_value': risk_value,
                'risk_level': 'HIGH' if risk_value > 0.7 else 'MEDIUM' if risk_value > 0.4 else 'LOW'
            })
        
        return risk_zones
    
    def generate_forecast(self, days=7):
        forecast_data = {
            'dates': [],
            'probabilities': [],
            'confidence_intervals': []
        }
        
        base_date = datetime.utcnow()
        base_prob = random.uniform(0.3, 0.6)
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            prob = base_prob + (i * 0.02) + random.uniform(-0.05, 0.05)
            prob = max(0, min(1, prob))
            
            forecast_data['dates'].append(date.isoformat())
            forecast_data['probabilities'].append(prob)
            forecast_data['confidence_intervals'].append([
                max(0, prob - 0.1),
                min(1, prob + 0.1)
            ])
        
        return forecast_data

# Initialize services
predictor = SimpleRockfallPredictor()
print("✅ Services initialized successfully")

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    """Receive and store sensor data"""
    try:
        data = request.json
        sensor_data = SensorData(
            sensor_id=data['sensor_id'],
            sensor_type=data['sensor_type'],
            location_x=data['location_x'],
            location_y=data['location_y'],
            value=data['value'],
            unit=data['unit'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )
        db.session.add(sensor_data)
        db.session.commit()
        
        # Trigger prediction if enough data
        if should_trigger_prediction():
            try:
                prediction_result = predictor.predict_rockfall_risk()
                process_prediction_result(prediction_result)
            except Exception as e:
                print(f"Prediction error: {e}")
        
        return jsonify({'status': 'success', 'id': sensor_data.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/risk-assessment', methods=['GET'])
def get_risk_assessment():
    """Get current risk assessment"""
    try:
        # Get latest risk assessment
        latest_assessment = RiskAssessment.query.order_by(RiskAssessment.timestamp.desc()).first()
        
        if not latest_assessment:
            return jsonify({'message': 'No risk assessment available'}), 404
        
        return jsonify({
            'risk_level': latest_assessment.risk_level,
            'probability': latest_assessment.probability,
            'affected_zones': json.loads(latest_assessment.affected_zones),
            'timestamp': latest_assessment.timestamp.isoformat(),
            'recommendations': json.loads(latest_assessment.recommendations) if latest_assessment.recommendations else []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk-map', methods=['GET'])
def get_risk_map():
    """Get risk map data for visualization"""
    try:
        # Get recent sensor data for risk mapping
        recent_data = SensorData.query.filter(
            SensorData.timestamp >= datetime.utcnow() - timedelta(hours=24)
        ).all()
        
        risk_zones = predictor.generate_risk_map(recent_data)
        
        return jsonify({
            'risk_zones': risk_zones,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get recent alerts"""
    try:
        alerts = Alert.query.filter(
            Alert.timestamp >= datetime.utcnow() - timedelta(days=7)
        ).order_by(Alert.timestamp.desc()).all()
        
        alert_list = []
        for alert in alerts:
            alert_list.append({
                'id': alert.id,
                'alert_type': alert.alert_type,
                'severity': alert.severity,
                'message': alert.message,
                'location': alert.location,
                'timestamp': alert.timestamp.isoformat(),
                'status': alert.status
            })
        
        return jsonify({'alerts': alert_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """Get rockfall probability forecast"""
    try:
        forecast_data = predictor.generate_forecast()
        return jsonify(forecast_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def should_trigger_prediction():
    """Determine if prediction should be triggered based on data availability"""
    recent_count = SensorData.query.filter(
        SensorData.timestamp >= datetime.utcnow() - timedelta(minutes=30)
    ).count()
    return recent_count >= 10  # Trigger if we have at least 10 recent readings

def process_prediction_result(prediction_result):
    """Process prediction result and generate alerts if necessary"""
    risk_level = prediction_result['risk_level']
    probability = prediction_result['probability']
    
    try:
        # Store risk assessment
        assessment = RiskAssessment(
            risk_level=risk_level,
            probability=probability,
            affected_zones=json.dumps(prediction_result['affected_zones']),
            recommendations=json.dumps(prediction_result['recommendations'])  # Convert to JSON string
        )
        db.session.add(assessment)
        
        # Generate alert if high risk
        if risk_level in ['HIGH', 'CRITICAL']:
            alert = Alert(
                alert_type='ROCKFALL_WARNING',
                severity=risk_level,
                message=f"High rockfall risk detected. Probability: {probability:.2%}",
                location=json.dumps(prediction_result['affected_zones'])
            )
            db.session.add(alert)
            
            # Send notifications (mock for now)
            print(f"🚨 Alert generated: {alert.message}")
        
        db.session.commit()
        print(f"✅ Risk assessment stored: {risk_level} ({probability:.1%})")
        
    except Exception as e:
        print(f"Database error: {e}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)