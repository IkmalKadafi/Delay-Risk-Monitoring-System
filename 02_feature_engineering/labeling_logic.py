"""
SLA Labeling Logic
==================

Purpose:
    - consistently generate target labels (Ground Truth) for training and evaluation.
    - Encapsulates the business definition of "Late".
    
Usage:
    - Called by the offline dataset preparation pipeline.
    - Can be imported by evaluation scripts to ensure metric consistency.

Author: Data Science Team
Stage: STAGE 2 - Feature Engineering
"""

import pandas as pd

def calculate_delivery_duration(df, start_col='task_created_time', end_col='delivery_time'):
    """
    Calculates the actual duration of the delivery process.
    
    Args:
        df (pd.DataFrame): DataFrame containing timestamp columns.
        start_col (str): Column name for process start (e.g., creation or pickup).
                         Default: 'task_created_time' (Customer View SLA).
        end_col (str): Column name for process end (e.g., delivered).
        
    Returns:
        pd.Series: Duration in minutes.
    """
    # Ensure datetime format
    start_ts = pd.to_datetime(df[start_col])
    end_ts = pd.to_datetime(df[end_col])
    
    # Calculate duration in minutes
    duration_minutes = (end_ts - start_ts).dt.total_seconds() / 60.0
    
    return duration_minutes

def assign_sla_label(duration_series, threshold_minutes=120):
    """
    Generates binary classification labels based on SLA threshold.
    
    Args:
        duration_series (pd.Series or float): Delivery duration in minutes.
        threshold_minutes (int): The SLA limit (e.g., 120 minutes for Express).
        
    Returns:
        pd.Series or int: 1 if Late (Violation), 0 if On-Time.
    """
    # Simply check if duration exceeds threshold
    # Note: Handling outliers or negative values (error data) should be done in cleaning step
    # Here we implement pure business logic
    
    labels = (duration_series > threshold_minutes).astype(int)
    
    return labels

def get_config_thresholds():
    """
    Returns standard thresholds for different service levels.
    """
    return {
        'instant': 60,      # 1 hour
        'same_day': 480,    # 8 hours
        'next_day': 1440    # 24 hours
    }
