"""
Evaluate Model Performance
==========================

Purpose:
    - Evaluate the trained XGBoost model using operationally relevant metrics.
    - Focus on Recall for the "Late" class (Class 1) because missing a potential delay 
      (False Negative) is costlier than a false alarm (False Positive).

Metrics:
    - ROC-AUC: General discrimination ability.
    - Precision vs Recall: Operational trade-off.
    - Confusion Matrix: Raw counts of correct/incorrect predictions.

Usage:
    - Run after train_xgboost.py creates the model artifact.

Author: Machine Learning Team
Stage: STAGE 3 - Predictive Modeling
"""

import xgboost as xgb
import pandas as pd
import joblib
import json
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score
import matplotlib.pyplot as plt # Optional, checking if user wants visual plots code (omitted for pure script)

# Configuration
MODEL_PATH = "sla_risk_model.json"
FEATURES_PATH = "model_features.pkl"
# Using the same data generation logic for demo purposes if file doesn't exist
DATA_PATH = "../02_feature_engineering/training_set_v1.parquet" 

# Operational Threshold (Decision Cutoff)
# Standard is 0.5, but in high-risk operations, we might lower it to catch more delays
DECISION_THRESHOLD = 0.5

def load_data_and_features():
    # Reuse loading logic (in production, import this from shared utility)
    # Re-generating validation set logic:
    if not os.path.exists(DATA_PATH):
        # ... (Same dummy generation as train script for consistency if file missing)
        import numpy as np
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
            "is_late": np.random.choice([0, 1], 1000, p=[0.8, 0.2]), 
            "partition_date": dates.date
        })
    else:
        df = pd.read_parquet(DATA_PATH)
        
    cols = joblib.load(FEATURES_PATH)
    
    # Re-create Val Split (Last 20%)
    df = df.sort_values("partition_date")
    split_idx = int(len(df) * 0.8)
    val_df = df.iloc[split_idx:]
    
    return val_df[cols], val_df["is_late"]

import os

def evaluate():
    print("Loading model and validation data...")
    if not os.path.exists(MODEL_PATH):
        print("Error: Model file not found. Run train_xgboost.py first.")
        return

    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    
    X_val, y_val = load_data_and_features()
    
    # 1. Generate Probabilities
    y_prob = model.predict_proba(X_val)[:, 1]
    
    # 2. Apply Decision Threshold
    y_pred = (y_prob >= DECISION_THRESHOLD).astype(int)
    
    # 3. Calculate Metrics
    auc = roc_auc_score(y_val, y_prob)
    acc = accuracy_score(y_val, y_pred)
    
    print("-" * 30)
    print(f"Global Metrics (Threshold={DECISION_THRESHOLD})")
    print("-" * 30)
    print(f"ROC-AUC:  {auc:.4f} (Ability to rank risk)")
    print(f"Accuracy: {acc:.4f} (Not primary metric due to imbalance)")
    print("")
    
    # 4. Detailed Classification Report
    # Focus on '1' (Late) Recall
    print("Classification Report:")
    print(classification_report(y_val, y_pred, target_names=["On-Time", "Late"]))
    
    # 5. Confusion Matrix (Business Impact)
    cm = confusion_matrix(y_val, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print("-" * 30)
    print("Operational Confusion Matrix")
    print("-" * 30)
    print(f"True Negatives  (Correctly On-Time): {tn}")
    print(f"False Positives (False Alarm)      : {fp} -> Wasted Intervention Cost")
    print(f"False Negatives (Missed Delay)     : {fn} -> SLA Breach Penalty (HIGH COST)")
    print(f"True Positives  (Caught Delay)     : {tp} -> Successful Intervention")
    print("-" * 30)
    
    # 6. Trade-off Interpretation
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    print(f"Late Recall: {recall:.2%} -> We catch {recall:.2%} of all actual delays.")
    
    if recall < 0.7:
        print("WARNING: Recall is below 70%. Consider lowering the decision threshold.")

if __name__ == "__main__":
    evaluate()
