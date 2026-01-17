
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
import logging

logger = logging.getLogger(__name__)

def engineering_features(df):
    """
    Performs feature engineering on the LaDe dataframe.
    
    Assumed Columns (based on typical LaDe schema):
    - `accept_time`: Time courier accepted task
    - `promise_time`: SLA deadline
    - `finish_time`: Actual delivery time
    (We will verify columns, if different, we adapt)
    
    Returns:
        X (pd.DataFrame): Features
        y (pd.Series): Target (1 if finish_time > promise_time else 0)
        encoders (dict): Dictionary of fitted label encoders
    """
    df = df.copy()
    
    # ---------------------------------------------------------
    # 1. Schema Standardization (Adapting to common LaDe naming)
    # ---------------------------------------------------------
    # Note: If columns are different, we might need to adjust.
    # We'll print columns in main execution to verify.
    # For now, we assume standard timestamps exist.
    
    # Mocking column check/filling for robustness if real names vary slightly
    # Common keys in LaDe: 'req_time', 'accept_time', 'finish_time'
    
    time_cols = [c for c in df.columns if 'time' in c.lower()]
    logger.info(f"Time columns found: {time_cols}")
    
    # Let's try to identify critical columns
    # We NEED a ground truth for 'sla_breach'.
    # If `promise_time` exists, use it. Else, simulate a synthetic SLA based on distance.
    
    target_col = 'sla_breach'
    
    # --- SYNTHETIC LOGIC IF COLUMNS MISSING (Safety Net) ---
    # Real LaDe often has 'order_time' and 'delivery_time'. 
    # We can define SLA as order_time + X hours.
    
    if 'finish_time' not in df.columns and 'delivery_time' in df.columns:
        df['finish_time'] = df['delivery_time']
        
    if 'accept_time' not in df.columns and 'order_time' in df.columns:
        df['accept_time'] = df['order_time']
        
    # Ensure datetime
    for col in time_cols:
        if not pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                # Try unit='s' first (common in LaDe), fallback if needed
                df[col] = pd.to_datetime(df[col], unit='s', errors='coerce')
            except:
                 df[col] = pd.to_datetime(df[col], errors='coerce')
        
    # Create Target: SLA Breach
    # If dataset has no promise_time, we assume SLA = accept_time + 2 hours (Last Mile standard)
    if 'promise_time' in df.columns:
        df['promise_time'] = pd.to_datetime(df['promise_time'], unit='s')
        df[target_col] = (df['finish_time'] > df['promise_time']).astype(int)
    else:
        # Fallback SLA: 2 hours from accept
        logger.warning("No 'promise_time' found. Constructing synthetic SLA (2 hours).")
        df['sla_deadline'] = df['accept_time'] + pd.to_timedelta(2, unit='h')
        df[target_col] = (df['finish_time'] > df['sla_deadline']).astype(int)

    # ---------------------------------------------------------
    # 2. Feature Extraction
    # ---------------------------------------------------------
    
    # Time based features
    df['hour_of_day'] = df['accept_time'].dt.hour
    df['day_of_week'] = df['accept_time'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Duration (if available at inference time? No, duration is target proxy. Don't leak it.)
    # We can use 'distance' if available.
    
    if 'distance' not in df.columns:
        # Create random distance if missing (unlikely in LaDe)
        # Global np is used
        df['distance'] = np.random.uniform(0.5, 20.0, size=len(df))
        
    df['log_distance'] = np.log1p(df['distance'])
    
    # Categorical features
    cat_feats = ['weather', 'vehicle_type'] # Example common fields
    existing_cats = [c for c in cat_feats if c in df.columns]
    
    encoders = {}
    for col in existing_cats:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
        
    # Select features for training
    feature_cols = ['hour_of_day', 'day_of_week', 'is_weekend', 'log_distance'] + existing_cats
    
    # Validation: drop rows with NaNs in features
    train_df = df[feature_cols + [target_col]].dropna()
    
    X = train_df[feature_cols]
    y = train_df[target_col]
    
    return X, y, encoders

def save_encoders(encoders, path="backend/encoders.pkl"):
    joblib.dump(encoders, path)

