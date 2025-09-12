from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)  # displacement, strain, pore_pressure, temperature, etc.
    location_x = db.Column(db.Float, nullable=False)
    location_y = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SensorData {self.sensor_id}: {self.value} {self.unit}>'

class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    risk_level = db.Column(db.String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    probability = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    affected_zones = db.Column(db.Text, nullable=False)  # JSON string of coordinates
    recommendations = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RiskAssessment {self.risk_level}: {self.probability:.2%}>'

class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text)  # JSON string of coordinates
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='ACTIVE')  # ACTIVE, ACKNOWLEDGED, RESOLVED
    
    def __repr__(self):
        return f'<Alert {self.alert_type}: {self.severity}>'

class DroneImagery(db.Model):
    __tablename__ = 'drone_imagery'
    
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    location_x = db.Column(db.Float, nullable=False)
    location_y = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Float)
    analysis_results = db.Column(db.Text)  # JSON string of analysis results
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DroneImagery {self.image_path}>'

class EnvironmentalData(db.Model):
    __tablename__ = 'environmental_data'
    
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String(50), nullable=False)  # rainfall, temperature, vibration
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    location_x = db.Column(db.Float)
    location_y = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EnvironmentalData {self.data_type}: {self.value} {self.unit}>'