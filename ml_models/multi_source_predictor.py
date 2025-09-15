import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib
import os
from datetime import datetime, timedelta
import json

class MultiSourceRockfallPredictor:
    """
    Advanced rockfall predictor that integrates multiple data sources:
    - Geotechnical sensor data
    - Drone imagery analysis
    - DEM (Digital Elevation Model) data
    - Satellite imagery
    - Environmental factors
    - Geological survey data
    """
    
    def __init__(self):
        self.classification_model = None
        self.regression_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        self.feature_importance = {}
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models if they exist"""
        try:
            if os.path.exists('ml_models/multi_source_classifier.pkl'):
                self.classification_model = joblib.load('ml_models/multi_source_classifier.pkl')
                self.regression_model = joblib.load('ml_models/multi_source_regressor.pkl')
                self.scaler = joblib.load('ml_models/multi_source_scaler.pkl')
                self.label_encoders = joblib.load('ml_models/multi_source_encoders.pkl')
                self.is_trained = True
                print("✅ Multi-source models loaded successfully")
        except Exception as e:
            print(f"⚠️ Loading models failed: {e}")
            self.train_initial_model()
    
    def generate_synthetic_multi_source_data(self, n_samples=2000):
        """Generate synthetic multi-source data for training"""
        np.random.seed(42)
        
        data = {
            # Geotechnical sensor data
            'displacement': np.random.normal(0.5, 0.3, n_samples),
            'strain': np.random.normal(100, 50, n_samples),
            'pore_pressure': np.random.normal(50, 20, n_samples),
            'vibration': np.random.exponential(0.1, n_samples),
            
            # Environmental factors
            'rainfall': np.random.exponential(5, n_samples),
            'temperature': np.random.normal(15, 10, n_samples),
            'humidity': np.random.normal(60, 20, n_samples),
            'wind_speed': np.random.exponential(3, n_samples),
            
            # Drone imagery analysis results
            'cracks_detected': np.random.poisson(2, n_samples),
            'vegetation_coverage': np.random.uniform(0, 80, n_samples),
            'rock_exposure': np.random.uniform(20, 100, n_samples),
            'thermal_anomalies': np.random.poisson(1, n_samples),
            
            # DEM analysis results
            'slope_angle': np.random.normal(45, 15, n_samples),
            'elevation_change': np.random.normal(0, 2, n_samples),
            'terrain_roughness': np.random.uniform(0, 10, n_samples),
            'critical_zones_percentage': np.random.uniform(0, 20, n_samples),
            
            # Satellite imagery analysis
            'vegetation_index': np.random.uniform(-1, 1, n_samples),
            'moisture_content': np.random.uniform(0, 100, n_samples),
            'land_cover_change': np.random.uniform(0, 10, n_samples),
            
            # Geological factors
            'rock_type': np.random.choice(['granite', 'limestone', 'sandstone', 'shale'], n_samples),
            'weathering_grade': np.random.choice(['fresh', 'slightly', 'moderately', 'highly', 'completely'], n_samples),
            'joint_density': np.random.uniform(0, 10, n_samples),
            'fault_proximity': np.random.exponential(100, n_samples),
            
            # Historical factors
            'previous_failures': np.random.poisson(0.5, n_samples),
            'maintenance_history': np.random.choice(['good', 'average', 'poor'], n_samples),
            'monitoring_duration': np.random.uniform(1, 60, n_samples)  # months
        }
        
        df = pd.DataFrame(data)
        
        # Create complex risk score based on multiple factors
        risk_score = (
            # Sensor data contribution (40%)
            (df['displacement'] > 1.0).astype(int) * 0.15 +
            (df['strain'] > 150).astype(int) * 0.10 +
            (df['pore_pressure'] > 70).astype(int) * 0.10 +
            (df['vibration'] > 0.2).astype(int) * 0.05 +
            
            # Environmental contribution (20%)
            (df['rainfall'] > 15).astype(int) * 0.10 +
            (df['temperature'] < 0).astype(int) * 0.05 +
            (df['humidity'] > 80).astype(int) * 0.05 +
            
            # Drone imagery contribution (15%)
            (df['cracks_detected'] > 3).astype(int) * 0.08 +
            (df['vegetation_coverage'] < 20).astype(int) * 0.04 +
            (df['thermal_anomalies'] > 2).astype(int) * 0.03 +
            
            # DEM contribution (15%)
            (df['slope_angle'] > 60).astype(int) * 0.08 +
            (df['critical_zones_percentage'] > 10).astype(int) * 0.07 +
            
            # Geological contribution (10%)
            (df['weathering_grade'].isin(['highly', 'completely'])).astype(int) * 0.05 +
            (df['joint_density'] > 7).astype(int) * 0.03 +
            (df['fault_proximity'] < 50).astype(int) * 0.02
        )
        
        # Add some noise and interactions
        risk_score += np.random.normal(0, 0.1, n_samples)
        
        # Interaction effects
        risk_score += ((df['rainfall'] > 10) & (df['slope_angle'] > 50)).astype(int) * 0.1
        risk_score += ((df['cracks_detected'] > 2) & (df['displacement'] > 0.8)).astype(int) * 0.15
        
        risk_score = np.clip(risk_score, 0, 1)
        
        df['rockfall_probability'] = risk_score
        df['rockfall_occurred'] = (risk_score > 0.6).astype(int)
        
        return df
    
    def prepare_features(self, df):
        """Prepare features for training/prediction"""
        # Encode categorical variables
        categorical_columns = ['rock_type', 'weathering_grade', 'maintenance_history']
        
        for col in categorical_columns:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col])
                else:
                    # Handle unseen categories
                    try:
                        df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])
                    except ValueError:
                        # Assign a default value for unseen categories
                        df[f'{col}_encoded'] = 0
        
        # Select numerical features
        feature_columns = [
            'displacement', 'strain', 'pore_pressure', 'vibration',
            'rainfall', 'temperature', 'humidity', 'wind_speed',
            'cracks_detected', 'vegetation_coverage', 'rock_exposure', 'thermal_anomalies',
            'slope_angle', 'elevation_change', 'terrain_roughness', 'critical_zones_percentage',
            'vegetation_index', 'moisture_content', 'land_cover_change',
            'joint_density', 'fault_proximity', 'previous_failures', 'monitoring_duration'
        ]
        
        # Add encoded categorical features
        for col in categorical_columns:
            if f'{col}_encoded' in df.columns:
                feature_columns.append(f'{col}_encoded')
        
        # Create interaction features
        df['displacement_slope_interaction'] = df['displacement'] * df['slope_angle']
        df['rainfall_vegetation_interaction'] = df['rainfall'] * (100 - df['vegetation_coverage'])
        df['cracks_thermal_interaction'] = df['cracks_detected'] * df['thermal_anomalies']
        
        feature_columns.extend([
            'displacement_slope_interaction',
            'rainfall_vegetation_interaction', 
            'cracks_thermal_interaction'
        ])
        
        return df[feature_columns]
    
    def train_initial_model(self):
        """Train initial model with synthetic multi-source data"""
        print("🤖 Training multi-source rockfall prediction model...")
        
        # Generate synthetic training data
        synthetic_data = self.generate_synthetic_multi_source_data(2000)
        
        # Prepare features
        X = self.prepare_features(synthetic_data)
        y_class = synthetic_data['rockfall_occurred']
        y_prob = synthetic_data['rockfall_probability']
        
        # Split data
        X_train, X_test, y_class_train, y_class_test, y_prob_train, y_prob_test = train_test_split(
            X, y_class, y_prob, test_size=0.2, random_state=42, stratify=y_class
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train classification model
        self.classification_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
        self.classification_model.fit(X_train_scaled, y_class_train)
        
        # Train regression model
        self.regression_model = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.regression_model.fit(X_train_scaled, y_prob_train)
        
        # Evaluate models
        class_pred = self.classification_model.predict(X_test_scaled)
        prob_pred = self.regression_model.predict(X_test_scaled)
        
        accuracy = accuracy_score(y_class_test, class_pred)
        mse = mean_squared_error(y_prob_test, prob_pred)
        
        print(f"✅ Classification Accuracy: {accuracy:.3f}")
        print(f"✅ Regression MSE: {mse:.3f}")
        
        # Calculate feature importance
        feature_names = X.columns.tolist()
        self.feature_importance = dict(zip(
            feature_names, 
            self.classification_model.feature_importances_
        ))
        
        # Save models
        self.save_models()
        self.is_trained = True
    
    def save_models(self):
        """Save trained models"""
        os.makedirs('ml_models', exist_ok=True)
        joblib.dump(self.classification_model, 'ml_models/multi_source_classifier.pkl')
        joblib.dump(self.regression_model, 'ml_models/multi_source_regressor.pkl')
        joblib.dump(self.scaler, 'ml_models/multi_source_scaler.pkl')
        joblib.dump(self.label_encoders, 'ml_models/multi_source_encoders.pkl')
        print("✅ Multi-source models saved successfully")
    
    def predict_rockfall_risk(self, multi_source_data=None):
        """Predict rockfall risk using multi-source data"""
        if not self.is_trained:
            return {'error': 'Model not trained'}
        
        # Use mock data if none provided
        if multi_source_data is None:
            multi_source_data = self.get_mock_multi_source_data()
        
        # Convert to DataFrame
        df = pd.DataFrame([multi_source_data])
        
        # Prepare features
        try:
            features = self.prepare_features(df)
            features_scaled = self.scaler.transform(features)
            
            # Make predictions
            rockfall_prob = self.regression_model.predict(features_scaled)[0]
            rockfall_class = self.classification_model.predict(features_scaled)[0]
            
            # Get prediction confidence
            class_proba = self.classification_model.predict_proba(features_scaled)[0]
            confidence = max(class_proba)
            
            # Determine risk level
            if rockfall_prob < 0.25:
                risk_level = 'LOW'
            elif rockfall_prob < 0.5:
                risk_level = 'MEDIUM'
            elif rockfall_prob < 0.75:
                risk_level = 'HIGH'
            else:
                risk_level = 'CRITICAL'
            
            # Generate detailed analysis
            analysis = self.generate_detailed_analysis(multi_source_data, features.iloc[0])
            
            return {
                'risk_level': risk_level,
                'probability': float(np.clip(rockfall_prob, 0, 1)),
                'confidence': float(confidence),
                'classification': int(rockfall_class),
                'data_sources_used': list(multi_source_data.keys()),
                'feature_contributions': self.get_feature_contributions(features.iloc[0]),
                'detailed_analysis': analysis,
                'recommendations': self.generate_enhanced_recommendations(risk_level, multi_source_data),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def get_mock_multi_source_data(self):
        """Generate mock multi-source data for demonstration"""
        return {
            # Sensor data
            'displacement': np.random.normal(0.8, 0.2),
            'strain': np.random.normal(120, 30),
            'pore_pressure': np.random.normal(60, 15),
            'vibration': np.random.exponential(0.08),
            
            # Environmental
            'rainfall': np.random.exponential(4),
            'temperature': np.random.normal(18, 5),
            'humidity': np.random.normal(65, 15),
            'wind_speed': np.random.exponential(2),
            
            # Drone analysis
            'cracks_detected': np.random.poisson(2),
            'vegetation_coverage': np.random.uniform(10, 60),
            'rock_exposure': np.random.uniform(40, 90),
            'thermal_anomalies': np.random.poisson(1),
            
            # DEM analysis
            'slope_angle': 52,
            'elevation_change': np.random.normal(0, 1),
            'terrain_roughness': np.random.uniform(3, 8),
            'critical_zones_percentage': np.random.uniform(5, 15),
            
            # Satellite analysis
            'vegetation_index': np.random.uniform(0.2, 0.8),
            'moisture_content': np.random.uniform(20, 80),
            'land_cover_change': np.random.uniform(0, 5),
            
            # Geological
            'rock_type': np.random.choice(['granite', 'limestone', 'sandstone']),
            'weathering_grade': np.random.choice(['slightly', 'moderately', 'highly']),
            'joint_density': np.random.uniform(3, 8),
            'fault_proximity': np.random.exponential(80),
            'previous_failures': np.random.poisson(0.3),
            'maintenance_history': np.random.choice(['good', 'average']),
            'monitoring_duration': np.random.uniform(6, 36)
        }
    
    def generate_detailed_analysis(self, data, features):
        """Generate detailed analysis of contributing factors"""
        analysis = {
            'sensor_analysis': {
                'displacement_status': 'high' if data['displacement'] > 1.0 else 'normal',
                'strain_status': 'elevated' if data['strain'] > 150 else 'normal',
                'pressure_status': 'high' if data['pore_pressure'] > 70 else 'normal'
            },
            'environmental_analysis': {
                'weather_risk': 'high' if data['rainfall'] > 10 else 'low',
                'temperature_impact': 'freeze_thaw' if data['temperature'] < 5 else 'normal'
            },
            'imagery_analysis': {
                'structural_integrity': 'compromised' if data['cracks_detected'] > 3 else 'stable',
                'vegetation_stability': 'poor' if data['vegetation_coverage'] < 20 else 'good'
            },
            'geological_analysis': {
                'slope_stability': 'critical' if data['slope_angle'] > 60 else 'stable',
                'weathering_impact': data['weathering_grade']
            }
        }
        
        return analysis
    
    def get_feature_contributions(self, features):
        """Get the contribution of each feature to the prediction"""
        contributions = {}
        
        for feature, importance in self.feature_importance.items():
            if feature in features.index:
                contributions[feature] = {
                    'importance': float(importance),
                    'value': float(features[feature])
                }
        
        # Sort by importance
        return dict(sorted(contributions.items(), key=lambda x: x[1]['importance'], reverse=True)[:10])
    
    def generate_enhanced_recommendations(self, risk_level, data):
        """Generate enhanced recommendations based on multi-source analysis"""
        recommendations = []
        
        # Base recommendations by risk level
        if risk_level == 'CRITICAL':
            recommendations.extend([
                "🚨 IMMEDIATE EVACUATION of all personnel from affected areas",
                "🛑 HALT all operations in high-risk zones immediately",
                "📞 ACTIVATE emergency response protocols",
                "🔄 CONTINUOUS monitoring required"
            ])
        elif risk_level == 'HIGH':
            recommendations.extend([
                "⚠️ RESTRICT access to affected areas",
                "📈 INCREASE monitoring frequency to hourly",
                "🚁 DEPLOY emergency response teams to standby",
                "📋 REVIEW and update evacuation procedures"
            ])
        elif risk_level == 'MEDIUM':
            recommendations.extend([
                "👁️ ENHANCED monitoring of affected zones",
                "📝 REVIEW safety protocols with personnel",
                "🔧 CONSIDER preventive stabilization measures"
            ])
        else:
            recommendations.append("✅ CONTINUE normal operations with regular monitoring")
        
        # Data-specific recommendations
        if data.get('rainfall', 0) > 10:
            recommendations.append("🌧️ HIGH RAINFALL: Monitor drainage systems and slope saturation")
        
        if data.get('displacement', 0) > 1.0:
            recommendations.append("📏 SIGNIFICANT DISPLACEMENT: Investigate slope stability immediately")
        
        if data.get('cracks_detected', 0) > 3:
            recommendations.append("🔍 MULTIPLE CRACKS: Conduct detailed structural assessment")
        
        if data.get('thermal_anomalies', 0) > 2:
            recommendations.append("🌡️ THERMAL ANOMALIES: Check for water infiltration or structural changes")
        
        if data.get('slope_angle', 0) > 60:
            recommendations.append("⛰️ STEEP SLOPE: Consider slope angle reduction or stabilization")
        
        if data.get('vegetation_coverage', 100) < 20:
            recommendations.append("🌱 LOW VEGETATION: Implement erosion control and revegetation")
        
        return recommendations