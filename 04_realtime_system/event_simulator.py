"""
Event Simulator (Stream Emulation)
==================================

Purpose:
    - Simulate a real-time stream of delivery events from historical data.
    - Serves as the "Source" for the Online System.
    - Mimics Kafka/Kinesis by yielding events sequentially.

Usage:
    - Run this script to feed events into the Online Feature Store.

Architecture Note:
    - In PRODUCTION, this script is replaced by:
      [Devices] -> [API Gateway] -> [Kafka Topic: 'raw-delivery-events']

Author: Real-Time Systems Team
Stage: STAGE 4 - Real-Time System
"""

import pandas as pd
import time
import json
from datetime import datetime

# Configuration
DATA_PATH = "../02_feature_engineering/training_set_v1.parquet" 
SIMULATION_SPEED = 1.0  # 1.0 = Real-time (slow), 100.0 = Fast-forward

def load_simulated_stream():
    """
    Load data and sort by time to mimic a stream.
    For this simulation, we use the `training_set_v1.parquet` which acts as our 'event log'.
    In reality, we would replay RAW event logs. Here we simulate 'Task Created' events based on features.
    """
    try:
        df = pd.read_parquet(DATA_PATH)
        # We don't have exact timestamps in this feature dataset, so we simulate proper ordering
        # assuming 'task_id' order or just sequential iteration for demo.
        print(f"Loaded {len(df)} records for simulation.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def emit_events(speed=1.0):
    """
    Generator that yields one event at a time.
    """
    df = load_simulated_stream()
    
    # Simulate sequential arrival
    for index, row in df.iterrows():
        # Construct an event payload similar to what a mobile app would send
        event_payload = {
            "event_id": f"evt_{index}",
            "event_type": "TASK_CREATED", # Primary trigger for risk scoring
            "timestamp": datetime.now().isoformat(), # Current simulation time
            "data": {
                "task_id": row.get('task_id', f"T{index}"),
                "courier_id": row.get('courier_id', f"C{index}"),
                # In a real stream, raw attributes are here. 
                # For this simulation, we pass pre-processed features to simplify the demo pipeline.
                "features": row.to_dict() 
            }
        }
        
        yield event_payload
        
        # Simulate latency between events
        time.sleep(0.1 / speed)

if __name__ == "__main__":
    print("Starting Stream Simulation...")
    for event in emit_events(speed=10.0): # 10x speed
        print(f"Streamed: {event['event_id']} - {event['event_type']}")
        if int(event['event_id'].split('_')[1]) > 5: break # Stop after 5 for basic test
    print("Stream Simulation Test Complete.")
