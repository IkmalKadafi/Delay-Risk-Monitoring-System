"""
Feature Importance Analysis
===========================

Purpose:
    - Extract feature importance from the trained XGBoost model.
    - Rank drivers of delay risk.
    - Categorize features into "Controllable" vs "External" for operations.

Output:
    - feature_importance.csv

Author: Machine Learning Team
Stage: STAGE 3 - Model Explainability
"""

import xgboost as xgb
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

MODEL_PATH = "sla_risk_model.json"
FEATURES_PATH = "model_features.pkl"
OUTPUT_CSV = "feature_importance.csv"

# Classification of Features for Business Context
FEATURE_CATEGORY_MAP = {
    "created_hour_sin": "External (Time)",
    "created_hour_cos": "External (Time)",
    "is_weekend": "External (Time)",
    "delivery_distance_km": "Semi-Controllable (Assignment)",
    "order_volume_last_1h": "External (Demand)",
    "courier_avg_speed_7d": "Controllable (Training/Selection)",
    "courier_late_rate_7d": "Controllable (Performance Mgmt)",
    "pickup_cluster": "External (Location)",
    "active_couriers_in_zone": "Controllable (Capacity Mgmt)"
}

def analyze_importance():
    if not os.path.exists(MODEL_PATH):
        print("Model not found.")
        return

    # Load Model
    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    
    # Load Feature Names (XGBoost loses names if saved as JSON sometimes)
    feature_names = joblib.load(FEATURES_PATH)
    
    # Extract Importance (Gain = improvement in accuracy brought by a feature)
    # Using 'gain' is generally better than 'weight' (frequency) for interpretation
    importance = model.booster.get_score(importance_type='gain')
    
    # Map raw feature names (f0, f1...) to actual names if needed
    # (XGBoost sklearn API usually handles this, but robust mapping below)
    
    # Create DataFrame
    # Note: booster.get_score returns dict {feature_name: score}
    # If the model uses actual feature names, keys are 'created_hour_sin', etc.
    
    df_imp = pd.DataFrame(list(importance.items()), columns=['Feature', 'Gain'])
    
    # Improve robustness if keys are missing (e.g., feature unused)
    # Fill missing features with 0
    existing = set(df_imp['Feature'])
    msg_rows = []
    for f in feature_names:
        if f not in existing:
            msg_rows.append({'Feature': f, 'Gain': 0})
    
    if msg_rows:
        df_imp = pd.concat([df_imp, pd.DataFrame(msg_rows)], ignore_index=True)

    # Add Operational Category
    df_imp['Category'] = df_imp['Feature'].map(FEATURE_CATEGORY_MAP).fillna("Other")
    
    # Sort
    df_imp = df_imp.sort_values("Gain", ascending=False).reset_index(drop=True)
    
    # Normalize Gain 0-100 for readability
    if df_imp['Gain'].max() > 0:
        df_imp['Relative_Importance'] = (df_imp['Gain'] / df_imp['Gain'].max()) * 100
    else:
        df_imp['Relative_Importance'] = 0

    print("-" * 60)
    print("TOP 10 RISK DRIVERS (By Information Gain)")
    print("-" * 60)
    print(df_imp.head(10)[['Feature', 'Relative_Importance', 'Category']].to_string(index=False))
    
    # Save
    df_imp.to_csv(OUTPUT_CSV, index=False)
    print(f"\nFull importance list saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    analyze_importance()
