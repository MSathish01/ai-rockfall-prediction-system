import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml_models'))

from rockfall_predictor import RockfallPredictor

# Create a global instance
predictor_instance = RockfallPredictor()

class RockfallPredictor:
    def __init__(self):
        self.predictor = predictor_instance
    
    def predict_rockfall_risk(self, sensor_data=None):
        return self.predictor.predict_rockfall_risk(sensor_data)
    
    def generate_risk_map(self, sensor_data_list):
        return self.predictor.generate_risk_map(sensor_data_list)
    
    def generate_forecast(self):
        return self.predictor.generate_forecast()