"""
Train XGBoost Model
===================

Purpose:
    - Train a gradient boosting model (XGBoost) to predict SLA breaches.
    - Uses time-series cross-validation logic (or time-based split) to prevent leakage.
    - Handles class imbalance typical in operations data.

Input:
    - Cleaned offline dataset (e.g., from 02_feature_engineering).

Output:
    - Trained Model Artifact (.json or .pkl).
    - Validation scores.

Author: Machine Learning Team
Stage: STAGE 3 - Predictive Modeling
"""

import xgboost as xgb
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics import roc_auc_score

# Configuration
# ----------------
# In production, these should be in a config.yaml
DATA_PATH = "../02_feature_engineering/training_set_v1.parquet"  # Assumption based on Stage 2
MODEL_OUTPUT_PATH = "sla_risk_model.json"
TARGET_COL = "is_late"
ID_COLS = ["task_id", "courier_id", "city_code", "partition_date"]
# Features to exclude from training (IDs + Target + Leaky features)
EXCLUDE_COLS = ID_COLS + [TARGET_COL, "delivery_duration_actual", "delivery_time"]

def load_data(path):
    """
    Load dataset. 
    Ideally this loads from a Feature Store or Data Warehouse.
    For this script, we assume a local parquet file or generate dummy data if missing.
    """
    if not os.path.exists(path):
        print(f"WARNING: Data file {path} not found. Generating detailed dummy data for demonstration.")
        # Generate dummy data with correct columns
        dates = pd.date_range(start="2023-01-01", periods=1000, freq="H")
        df = pd.DataFrame({
            "task_id": [f"T{i}" for i in range(1000)],
            "created_hour_sin": np.random.rand(1000),
            "created_hour_cos": np.random.rand(1000),
            "is_weekend": np.random.randint(0, 2, 1000),
            "delivery_distance_km": np.random.uniform(1, 20, 1000),
            "order_volume_last_1h": np.random.randint(10, 500, 1000),
            "courier_avg_speed_7d": np.random.uniform(20, 60, 1000),
            "courier_late_rate_7d": np.random.uniform(0, 0.5, 1000),
            "is_late": np.random.choice([0, 1], 1000, p=[0.8, 0.2]), # Imbalanced
            "partition_date": dates.date
        })
        return df
    return pd.read_parquet(path)

def train_model():
    print("Loading data...")
    df = load_data(DATA_PATH)
    
    # 1. Time-Based Split (Critical for Time-Series/Logistics)
    # Train: First 80% of data (by time)
    # Val: Last 20%
    # This prevents "future leakage" where model learns from future patterns.
    
    df = df.sort_values("partition_date")
    split_idx = int(len(df) * 0.8)
    
    train_df = df.iloc[:split_idx]
    val_df = df.iloc[split_idx:]
    
    print(f"Train set: {len(train_df)} rows")
    print(f"Val set:   {len(val_df)} rows")
    
    # Prepare X and y
    feature_cols = [c for c in df.columns if c not in EXCLUDE_COLS]
    print(f"Features ({len(feature_cols)}): {feature_cols}")
    
    X_train = train_df[feature_cols]
    y_train = train_df[TARGET_COL]
    
    X_val = val_df[feature_cols]
    y_val = val_df[TARGET_COL]
    
    # 2. Handle Class Imbalance
    # Calculate scale_pos_weight: sum(negative instances) / sum(positive instances)
    num_neg = (y_train == 0).sum()
    num_pos = (y_train == 1).sum()
    
    scale_weight = 1
    if num_pos > 0:
        scale_weight = num_neg / num_pos
    
    print(f"Class Imbalance Ratio (Neg/Pos): {scale_weight:.2f}")
    
    # 3. Initialize XGBoost
    # Using specific operational hyperparameters (standard baseline)
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        n_estimators=200,          # Sufficient trees
        learning_rate=0.05,        # Conservative learning rate
        max_depth=5,               # Prevent overfitting on specific features
        scale_pos_weight=scale_weight, # HANDLING IMBALANCE
        eval_metric='auc',
        early_stopping_rounds=20,
        n_jobs=-1,
        random_state=42
    )
    
    print("Training model...")
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        verbose=10
    )
    
    # 4. Basic Validation
    val_probs = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, val_probs)
    print(f"Validation AUC: {auc:.4f}")
    
    # 5. Save Artifacts
    model.save_model(MODEL_OUTPUT_PATH)
    print(f"Model saved to {MODEL_OUTPUT_PATH}")
    
    # Also save the feature names for inference verification
    joblib.dump(feature_cols, "model_features.pkl")

if __name__ == "__main__":
    train_model()
