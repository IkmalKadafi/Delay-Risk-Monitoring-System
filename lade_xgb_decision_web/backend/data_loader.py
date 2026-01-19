
import os
import pandas as pd
import numpy as np
from datasets import load_dataset
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CACHE_DIR = "data_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) using NumPy.
    All inputs must be of same length.
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

def process_gps_to_orders(df):
    """
    Transforms raw GPS trajectory data into 'Order' records.
    Assumes columns: ['ds', 'postman_id', 'gps_time', 'lat', 'lng']
    """
    logger.info("Transforming raw GPS trajectories to Order/Route records...")
    
    # 1. Sort
    df = df.sort_values(by=['postman_id', 'ds', 'gps_time'])
    
    # 2. Group by Courier & Day to form a "Route"
    # For this dataset, we'll treat a full day's route as one "Job/Order" 
    # (or you could split by idle time, but Daily Performance is a good unit).
    
    grouped = df.groupby(['postman_id', 'ds'])
    
    processed_rows = []
    
    for (pid, ds), group in grouped:
        if len(group) < 2:
            continue
            
        # Extract basic info
        start_time = group['gps_time'].min()
        end_time = group['gps_time'].max()
        
        # Calculate Total Distance
        # Shift distinct points to handle stationary periods
        lats = group['lat'].values
        lngs = group['lng'].values
        
        # Vectorized distance calc
        dist_km = np.sum(haversine_np(lngs[:-1], lats[:-1], lngs[1:], lats[1:]))
        
        # Meta-data
        record = {
            'courier_id': int(pid) if not pd.isna(pid) else 0,
            'ds': ds,
            'accept_time': pd.to_datetime(start_time, unit='s'),
            'finish_time': pd.to_datetime(end_time, unit='s'),
            'distance': dist_km,
            # Synthetic features where missing
            'vehicle_type': 'Motorcycle', 
            'weather': 'Cloudy' # Placeholder
        }
        processed_rows.append(record)
        
    orders_df = pd.DataFrame(processed_rows)
    
    if orders_df.empty:
        logger.warning("Transformation resulted in empty dataframe!")
        return pd.DataFrame()

    # 3. Add SLA Logic (Promise Time)
    # Realistic assumption: 5 mins/km + 30 mins fixed
    avg_speed_min_per_km = 5.0 
    orders_df['promise_duration'] = orders_df['distance'] * avg_speed_min_per_km + 30
    orders_df['promise_time'] = orders_df['accept_time'] + pd.to_timedelta(orders_df['promise_duration'], unit='m')
    
    logger.info(f"Generated {len(orders_df)} order records from trajectories.")
    return orders_df

def load_lade_data(subset="default", split="train", sample_size=None, cache_path="data_cache/lade_orders.parquet"):
    """
    Loads LaDe data, forcing a fresh download/transform if needed to get real orders.
    """
    
    # Check cache first
    # IMPORTANT: We changed the cache filename to 'lade_orders' to distinguish from raw
    if os.path.exists(cache_path):
        logger.info(f"Loading transformed orders from cache: {cache_path}")
        df = pd.read_parquet(cache_path)
        if sample_size and len(df) > sample_size:
            df = df.sample(n=sample_size, random_state=42)
        return df

    logger.info(f"Downloading {subset} dataset from HuggingFace...")
    try:
        # We need ENOUGH rows to form routes. 20k rows might form ~50-100 routes.
        # Let's pull more to be safe -> 50,000
        download_limit = 100000 
        
        dataset = load_dataset("Cainiao-AI/LaDe", split=split, streaming=True, trust_remote_code=True)
        
        data_list = []
        for i, item in enumerate(dataset):
            data_list.append(item)
            if i >= download_limit:
                break
                
        raw_df = pd.DataFrame(data_list)
        logger.info(f"Downloaded {len(raw_df)} raw GPS points.")
        
        # TRANSFORM
        orders_df = process_gps_to_orders(raw_df)
        
        if orders_df.empty:
             # Fallback if transformation fails (e.g. data is not trajectory)
             raise ValueError("Transformation yielded 0 orders.")
             
        # Save cache
        logger.info(f"Saving transformed data to cache: {cache_path}")
        orders_df.to_parquet(cache_path, index=False)
        
        if sample_size and len(orders_df) > sample_size:
             return orders_df.sample(n=sample_size, random_state=42)
             
        return orders_df
        
    except Exception as e:
        logger.error(f"Error loading/transforming dataset: {e}")
        # Last resort fallback if real data fails completely
        # But we really want to avoid this now.
        logger.warning("Critical failure in real data load. Returning empty to signal issue.")
        return pd.DataFrame()

if __name__ == "__main__":
    df = load_lade_data(sample_size=10)
    print("Transformed Data Sample:")
    print(df.head())
    print("Columns:", df.columns)
