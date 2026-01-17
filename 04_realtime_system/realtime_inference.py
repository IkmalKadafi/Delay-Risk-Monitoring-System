"""
Real-Time Inference Service
===========================

Purpose:
    - Load the trained XGBoost model.
    - Accept Feature Vectors.
    - Return SLA Risk Probability.

Performance Requirements:
    - Latency: < 50ms per prediction.
    - No caching (inputs change per event).

Author: ML Engineering Team
Stage: STAGE 4 - Real-Time System
"""

import xgboost as xgb
import pandas as pd
import joblib
import os
import sys

# Add parent dir to path to import Stage 3 components if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

MODEL_PATH = "../03_modeling/sla_risk_model.json"
FEATURES_PATH = "../03_modeling/model_features.pkl"

class ModelService:
    def __init__(self):
        self.model = None
        self.feature_names = []
        self._load_model()
        
    def _load_model(self):
        """
        Load model artifact into memory (Cold Start).
        """
        if not os.path.exists(MODEL_PATH):
            print("WARNING: Model artifact not found. Inference will fail.")
            return

        print("Loading XGBoost Model...")
        self.model = xgb.XGBClassifier()
        self.model.load_model(MODEL_PATH)
        
        # Load feature names to ensure alignment
        if os.path.exists(FEATURES_PATH):
            self.feature_names = joblib.load(FEATURES_PATH)
        print(f"Model Loaded. Expecting {len(self.feature_names)} features.")

    def predict(self, feature_vector):
        """
        Generate risk probability.
        
        Args:
            feature_vector (dict): Feature dictionary from Feature Store.
            
        Returns:
            float: Probability (0.0 to 1.0) of 'Late' class.
        """
        if not self.model:
            return 0.5 # Fallback
            
        # Convert dictionary to DataFrame with correct ordering
        # XGBoost requires columns to be in EXACT training order
        try:
            # Filter dict to only known features
            input_data = {k: [v] for k, v in feature_vector.items() if k in self.feature_names}
            
            # Create DF and Fill missing cols with 0 (or NaN depending on training)
            df = pd.DataFrame(input_data)
            
            # Align columns
            for col in self.feature_names:
                if col not in df.columns:
                    df[col] = 0 # Impute missing operational data
                    
            df = df[self.feature_names] # Reorder strictly
            
            # Predict
            prob = self.model.predict_proba(df)[0][1]
            return float(prob)
            
        except Exception as e:
            print(f"Inference Error: {e}")
            return -1.0

# Unit Test
if __name__ == "__main__":
    svc = ModelService()
    # Mock features
    mock_input = {"delivery_distance_km": 12.5, "courier_avg_speed_7d": 45.0} # Partial input
    score = svc.predict(mock_input)
    print(f"Predicted Risk Probability: {score}")
