import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib
import os
from datetime import datetime, timedelta
import json

class RockfallPredictor:
    def __init__(self):
        self.classification_model = None
        self.regression_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models if they exist"""
        try:
            if os.path.exists('ml_models/rockfall_classifier.pkl'):
                self.classification_model = joblib.load('ml_models/rockfall_classifier.pkl')
                self.regression_model = joblib.load('ml_models/rockfall_regressor.pkl')
                self.scaler = joblib.load('ml_models/scaler.pkl')
                self.is_trained = True
                print("Models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            self.train_initial_model()
    
    def train_initial_model(self):
        """Train initial model with synthetic data"""
        print("Training initial model with synthetic data...")
        
        # Generate synthetic training data
        synthetic_data = self.generate_synthetic_data(1000)
        
        # Prepare features and targets
        X = synthetic_data[['displacement', 'strain', 'pore_pressure', 'rainfall', 
                          'temperature', 'vibration', 'slope_angle', 'rock_strength']]
        y_class = synthetic_data['rockfall_occurred']
        y_prob = synthetic_data['rockfall_probability']
        
        # Split data
        X_train, X_test, y_class_train, y_class_test, y_prob_train, y_prob_test = train_test_split(
            X, y_class, y_prob, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train classification model (rockfall occurrence)
        self.classification_model = RandomForestClassifier(
            n_estimators=100, random_state=42, max_depth=10
        )
        self.classification_model.fit(X_train_scaled, y_class_train)
        
        # Train regression model (rockfall probability)
        self.regression_model = GradientBoostingRegressor(
            n_estimators=100, random_state=42, max_depth=6
        )
        self.regression_model.fit(X_train_scaled, y_prob_train)
        
        # Evaluate models
        class_pred = self.classification_model.predict(X_test_scaled)
        prob_pred = self.regression_model.predict(X_test_scaled)
        
        print(f"Classification Accuracy: {accuracy_score(y_class_test, class_pred):.3f}")
        print(f"Regression MSE: {mean_squared_error(y_prob_test, prob_pred):.3f}")
        
        # Save models
        self.save_models()
        self.is_trained = True
    
    def generate_synthetic_data(self, n_samples):
        """Generate synthetic training data for rockfall prediction"""
        np.random.seed(42)
        
        data = {
            'displacement': np.random.normal(0.5, 0.3, n_samples),  # mm
            'strain': np.random.normal(100, 50, n_samples),  # microstrain
            'pore_pressure': np.random.normal(50, 20, n_samples),  # kPa
            'rainfall': np.random.exponential(5, n_samples),  # mm/day
            'temperature': np.random.normal(15, 10, n_samples),  # °C
            'vibration': np.random.exponential(0.1, n_samples),  # m/s²
            'slope_angle': np.random.normal(45, 15, n_samples),  # degrees
            'rock_strength': np.random.normal(50, 20, n_samples)  # MPa
        }
        
        df = pd.DataFrame(data)
        
        # Create target variables based on realistic relationships
        risk_score = (
            (df['displacement'] > 1.0).astype(int) * 0.3 +
            (df['strain'] > 150).astype(int) * 0.2 +
            (df['pore_pressure'] > 70).astype(int) * 0.2 +
            (df['rainfall'] > 10).astype(int) * 0.15 +
            (df['vibration'] > 0.2).astype(int) * 0.1 +
            (df['slope_angle'] > 60).astype(int) * 0.05
        )
        
        # Add some noise
        risk_score += np.random.normal(0, 0.1, n_samples)
        risk_score = np.clip(risk_score, 0, 1)
        
        df['rockfall_probability'] = risk_score
        df['rockfall_occurred'] = (risk_score > 0.6).astype(int)
        
        return df
    
    def save_models(self):
        """Save trained models"""
        os.makedirs('ml_models', exist_ok=True)
        joblib.dump(self.classification_model, 'ml_models/rockfall_classifier.pkl')
        joblib.dump(self.regression_model, 'ml_models/rockfall_regressor.pkl')
        joblib.dump(self.scaler, 'ml_models/scaler.pkl')
        print("Models saved successfully")
    
    def predict_rockfall_risk(self, sensor_data=None):
        """Predict rockfall risk based on current sensor data"""
        if not self.is_trained:
            return {'error': 'Model not trained'}
        
        # If no data provided, use mock data for demonstration
        if sensor_data is None:
            sensor_data = self.get_mock_sensor_data()
        
        # Prepare features
        features = np.array([[
            sensor_data.get('displacement', 0.5),
            sensor_data.get('strain', 100),
            sensor_data.get('pore_pressure', 50),
            sensor_data.get('rainfall', 5),
            sensor_data.get('temperature', 15),
            sensor_data.get('vibration', 0.1),
            sensor_data.get('slope_angle', 45),
            sensor_data.get('rock_strength', 50)
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make predictions
        rockfall_prob = self.regression_model.predict(features_scaled)[0]
        rockfall_class = self.classification_model.predict(features_scaled)[0]
        
        # Determine risk level
        if rockfall_prob < 0.2:
            risk_level = 'LOW'
        elif rockfall_prob < 0.4:
            risk_level = 'MEDIUM'
        elif rockfall_prob < 0.7:
            risk_level = 'HIGH'
        else:
            risk_level = 'CRITICAL'
        
        # Generate affected zones (mock coordinates)
        affected_zones = self.generate_affected_zones(rockfall_prob)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(risk_level, sensor_data)
        
        return {
            'risk_level': risk_level,
            'probability': float(rockfall_prob),
            'classification': int(rockfall_class),
            'affected_zones': affected_zones,
            'recommendations': recommendations,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_mock_sensor_data(self):
        """Generate mock sensor data for demonstration"""
        return {
            'displacement': np.random.normal(0.8, 0.2),
            'strain': np.random.normal(120, 30),
            'pore_pressure': np.random.normal(60, 15),
            'rainfall': np.random.exponential(3),
            'temperature': np.random.normal(18, 5),
            'vibration': np.random.exponential(0.05),
            'slope_angle': 52,
            'rock_strength': 45
        }
    
    def generate_affected_zones(self, probability):
        """Generate affected zone coordinates based on probability"""
        base_zones = [
            {'lat': -23.5505, 'lng': -46.6333, 'radius': 50},  # Zone 1
            {'lat': -23.5515, 'lng': -46.6343, 'radius': 75},  # Zone 2
            {'lat': -23.5525, 'lng': -46.6353, 'radius': 100}  # Zone 3
        ]
        
        # Adjust zones based on probability
        affected_zones = []
        for i, zone in enumerate(base_zones):
            if probability > (0.3 + i * 0.2):
                zone_copy = zone.copy()
                zone_copy['risk_level'] = min(int(probability * 10), 10)
                affected_zones.append(zone_copy)
        
        return affected_zones
    
    def generate_recommendations(self, risk_level, sensor_data):
        """Generate recommendations based on risk level and sensor data"""
        recommendations = []
        
        if risk_level == 'CRITICAL':
            recommendations.extend([
                "IMMEDIATE EVACUATION of personnel from affected areas",
                "Halt all operations in high-risk zones",
                "Deploy emergency response teams",
                "Continuous monitoring required"
            ])
        elif risk_level == 'HIGH':
            recommendations.extend([
                "Restrict access to affected areas",
                "Increase monitoring frequency",
                "Prepare evacuation procedures",
                "Review slope stability measures"
            ])
        elif risk_level == 'MEDIUM':
            recommendations.extend([
                "Enhanced monitoring of affected zones",
                "Review safety protocols",
                "Consider preventive measures"
            ])
        else:
            recommendations.append("Continue normal operations with regular monitoring")
        
        # Add specific recommendations based on sensor readings
        if sensor_data.get('rainfall', 0) > 10:
            recommendations.append("High rainfall detected - monitor drainage systems")
        
        if sensor_data.get('displacement', 0) > 1.0:
            recommendations.append("Significant displacement detected - investigate slope stability")
        
        return recommendations
    
    def generate_risk_map(self, sensor_data_list):
        """Generate risk map data for visualization"""
        risk_zones = []
        
        # Process each sensor location
        for i in range(10):  # Generate 10 risk zones for demonstration
            lat = -23.5505 + (i * 0.001)
            lng = -46.6333 + (i * 0.001)
            
            # Mock risk calculation
            risk_value = np.random.uniform(0, 1)
            
            risk_zones.append({
                'lat': lat,
                'lng': lng,
                'risk_value': risk_value,
                'risk_level': 'HIGH' if risk_value > 0.7 else 'MEDIUM' if risk_value > 0.4 else 'LOW'
            })
        
        return risk_zones
    
    def generate_forecast(self, days=7):
        """Generate rockfall probability forecast"""
        forecast_data = {
            'dates': [],
            'probabilities': [],
            'confidence_intervals': []
        }
        
        base_date = datetime.utcnow()
        base_prob = np.random.uniform(0.2, 0.6)
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            # Add some trend and noise
            prob = base_prob + (i * 0.02) + np.random.normal(0, 0.05)
            prob = np.clip(prob, 0, 1)
            
            forecast_data['dates'].append(date.isoformat())
            forecast_data['probabilities'].append(float(prob))
            forecast_data['confidence_intervals'].append([
                float(max(0, prob - 0.1)),
                float(min(1, prob + 0.1))
            ])
        
        return forecast_data