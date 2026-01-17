
import xgboost as xgb
import joblib
import pandas as pd
import os
import logging
from feature_engineering import engineering_features

logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self, model_path="model.pkl", encoder_path="encoders.pkl"):
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.model = None
        self.encoders = None
        self._load_artifacts()

    def _load_artifacts(self):
        if os.path.exists(self.model_path):
            # self.model = xgb.XGBClassifier()
            # self.model.load_model(self.model_path)
            self.model = joblib.load(self.model_path)
            logger.info("Model loaded.")
        else:
            logger.warning(f"Model file not found at {self.model_path}")
            
        if os.path.exists(self.encoder_path):
            self.encoders = joblib.load(self.encoder_path)
            logger.info("Encoders loaded.")
        else:
            logger.warning(f"Encoder file not found at {self.encoder_path}")

    def predict(self, input_data):
        """
        Predicts SLA breach probability for input data.
        Args:
            input_data (dict or list of dicts): Raw input features.
        Returns:
            list: Probabilities.
        """
        if not self.model:
            raise ValueError("Model not loaded. Train model first.")
            
        df = pd.DataFrame(input_data)
        
        # Preprocess
        # Note: engineering_features expects a certain schema and might re-fit label encoders if we aren't careful.
        # We need a transformation-only version. 
        # For simplicity, we assume we use the same function but for single row inference we must handle encoders carefully.
        # Actually, `engineering_features` returns `encoders` which implies it fits them.
        # We should modify `engineering_features` to accept `encoders` for transform only, OR handle it here.
        
        # Simplification: We will just re-use the logic but apply saved encoders for categoricals.
        
        # 1. Feature extraction logic (copy-paste/import from FE but handling transform)
        # We'll use the imported function but we need to ensure we don't re-fit encoders.
        # Refactoring FE to separate fit/transform is best, but due to time, I will apply encoders manually here 
        # matching what FE does.
        
        # Reuse time features
        time_cols = ['accept_time'] # Adjust based on input schema
        # Input expected: {'accept_time': '...', 'distance': ...}
        
        # If input is raw JSON, ensure format
        if 'accept_time' in df.columns:
             df['accept_time'] = pd.to_datetime(df['accept_time'])
             df['hour_of_day'] = df['accept_time'].dt.hour
             df['day_of_week'] = df['accept_time'].dt.dayofweek
             df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        if 'distance' in df.columns:
            import numpy as np
            df['log_distance'] = np.log1p(df['distance'])
            
        # Categoricals
        cat_feats = ['weather', 'vehicle_type']
        if self.encoders:
            for col in cat_feats:
                if col in df.columns and col in self.encoders:
                    # Handle unseen labels carefully
                    le = self.encoders[col]
                    df[col] = df[col].astype(str).map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        
        # Select columns matches training
        feature_cols = ['hour_of_day', 'day_of_week', 'is_weekend', 'log_distance'] + [c for c in cat_feats if c in df.columns]
        
        X = df[feature_cols]
        
        probs = self.model.predict_proba(X)[:, 1]
        return probs.tolist()

# Singleton instance
# engine = InferenceEngine()
