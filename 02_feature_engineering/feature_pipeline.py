"""
Feature Engineering Pipeline
============================

Purpose:
    - Transform raw event-level delivery data into task-level feature vectors.
    - Designed for offline batch processing (historical training data generation).
    - Modular design allows adaptation for future online/streaming inference.

Input Schema (Expected):
    - Raw event logs containing: task_id, courier_id, event_type, timestamp, city, etc.
    - See 01_data_foundation/data_schema.md for details.

Output:
    - Pandas DataFrame where 1 Row = 1 Delivery Task
    - Columns = Feature Vector

Author: Data Science Team
Stage: STAGE 2 - Feature Engineering & Offline Dataset Preparation
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ==========================================
# 1. TEMPORAL FEATURE EXTRACTION
# ==========================================

def extract_temporal_features(df):
    """
    Extracts time-based features from the task creation or assignment timestamp.
    
    Business Logic:
    - Delivery performance varies significantly by time of day (traffic) and day of week (volume).
    """
    # Ensure timestamp is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['task_created_time']):
        df['task_created_time'] = pd.to_datetime(df['task_created_time'])

    df['created_hour'] = df['task_created_time'].dt.hour
    df['created_day_of_week'] = df['task_created_time'].dt.dayofweek # 0=Mon, 6=Sun
    df['is_weekend'] = df['created_day_of_week'].isin([5, 6]).astype(int)
    
    # Cyclic encoding for hour (preserves 23:00 -> 00:00 continuity)
    df['created_hour_sin'] = np.sin(2 * np.pi * df['created_hour'] / 24)
    df['created_hour_cos'] = np.cos(2 * np.pi * df['created_hour'] / 24)
    
    return df

# ==========================================
# 2. OPERATIONAL & GEOGRAPHIC FEATURES
# ==========================================

def extract_location_features(df):
    """
    Extracts location-specific features.
    
    Business Logic:
    - Certain cities or zones have inherent congestion or difficulty levels.
    """
    # One-hot encoding for City (Top N cities, others as 'Other')
    # Note: In production, use a fitted encoder. Here is logical demonstration.
    if 'city' in df.columns:
        # Simple dummy encoding for demonstration
        city_dummies = pd.get_dummies(df['city'], prefix='loc_city')
        df = pd.concat([df, city_dummies], axis=1)
    
    return df

def calculate_distance_features(df):
    """
    Calculates distance metrics if coordinates are available.
    """
    if {'origin_lat', 'origin_lon', 'dest_lat', 'dest_lon'}.issubset(df.columns):
        # Haversine distance approximation or similar
        # For this pipeline, we assume 'distance_km' might be pre-calculated or raw
        pass 
    
    return df

# ==========================================
# 3. AGGREGATION LOGIC (Event to Task)
# ==========================================

def aggregate_events_to_task(events_df):
    """
    Aggregates a stream of raw events into a single row per task.
    
    Args:
        events_df: DataFrame of raw events (multiple rows per task)
        
    Returns:
        tasks_df: DataFrame with unique task_id and aggregated attributes
    """
    # Sort by task and time
    events_df = events_df.sort_values(['task_id', 'event_timestamp'])
    
    # 1. Identify critical timestamps per task
    # We want to pivot specific event types to columns
    # e.g., created, assigned, pickup, delivered
    
    # Filter for relevant event types
    # Assuming event_type values: 'TASK_CREATED', 'COURIER_ASSIGNED', 'PICKUP', 'DELIVERED'
    
    pivoted = events_df.pivot_table(
        index='task_id', 
        columns='event_type', 
        values='event_timestamp', 
        aggfunc='first' # Take first occurrence
    ).reset_index()
    
    # Rename columns for clarity (standardizing naming)
    # Note: Actual event type strings depend on LaDe dataset specific values
    column_map = {
        'TASK_CREATED': 'task_created_time',
        'COURIER_ASSIGNED': 'task_assigned_time',
        'PICKUP': 'pickup_time',
        'DELIVERED': 'delivery_time'
    }
    pivoted.rename(columns=column_map, inplace=True)
    
    # 2. Merge back static info (courier_id, city, etc.) from the first event or task creation event
    static_info = events_df.groupby('task_id').first()[['courier_id', 'city']]
    
    final_task_df = pd.merge(pivoted, static_info, on='task_id', how='left')
    
    return final_task_df

# ==========================================
# 4. COURIER HISTORY FEATURES (Advanced)
# ==========================================

def attach_courier_history(df, courier_stats_db=None):
    """
    Attaches historical performance data for the assigned courier.
    
    Business Logic:
    - Courier past performance (speed, success rate) is a strong predictor of future delay.
    - IMPORTANT: Must avoid target leakage. Use statistics calculated from data PRIOR to the current task.
    """
    # Placeholder for joining with a Feature Store or pre-computed stats dictionary
    # Example feature: courier_avg_delivery_time_last_7d
    
    # df['courier_avg_speed'] = df['courier_id'].map(courier_stats_db)
    return df

# ==========================================
# MASTER PIPELINE ORCHESTRATOR
# ==========================================

def run_feature_pipeline(raw_events_path):
    """
    Main function to execute the pipeline.
    
    1. Load Raw Data
    2. Aggregate Events -> Tasks
    3. Feature Engineering (Temporal, Geo, Operational)
    4. Return Model-Ready DataFrame (Features only, no Labels)
    """
    print("Starting Feature Engineering Pipeline...")
    
    # 1. Load Data (Demonstration)
    # df_events = pd.read_csv(raw_events_path) 
    
    # For demonstration, we create a mock DataFrame structure
    # In production, this comes from data_ingestion.py output or data warehouse
    print("...Loading raw events data")
    
    # 2. Aggregation
    # df_tasks = aggregate_events_to_task(df_events)
    # Mocking the result of aggregation for the pipeline flow
    df_tasks = pd.DataFrame({
        'task_id': ['T001', 'T002'],
        'task_created_time': [datetime(2023, 10, 27, 8, 30), datetime(2023, 10, 27, 9, 15)],
        'city': ['Jakarta', 'Bandung'],
        'courier_id': ['C001', 'C002']
    })
    
    print("...Aggregating events to task level")

    # 3. Feature Engineering
    df_features = extract_temporal_features(df_tasks)
    df_features = extract_location_features(df_features)
    
    # 4. Cleanup
    # Drop raw timestamps if not needed for model (keep 'created_hour' etc.)
    # Keep task_id for joining, but exclude from training
    
    print("Feature Pipeline Completed.")
    print(f"Generated Features: {list(df_features.columns)}")
    
    return df_features

if __name__ == "__main__":
    # Test run
    run_feature_pipeline("dummy_path.csv")
