
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np
import logging
from typing import List, Optional

from inference import InferenceEngine
from what_if import SimulationEngine
from analytics import get_dashboard_stats
from cost_evaluation import estimate_risk_exposure
# We'll use a globally loaded dataframe for the 'dataset' view and stats
from data_loader import load_lade_data

app = FastAPI(title="LaDe Analytics Platform")

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Global State ---
model_engine = InferenceEngine() # Loads model
simulation_engine = SimulationEngine() # Loads validation preds

# Cache a sample of data for the 'Dataset' page
try:
    # Use cached parquet if available for speed
    # We re-use load_lade_data logic which checks cache
    # We just need a sample for display
    DATA_SAMPLE = load_lade_data(sample_size=100)
    # Convert timestamps to string for JSON serialization
    for col in DATA_SAMPLE.select_dtypes(include=['datetime64[ns]']).columns:
        DATA_SAMPLE[col] = DATA_SAMPLE[col].astype(str)
except Exception as e:
    logger.error(f"Failed to load data sample: {e}")
    DATA_SAMPLE = pd.DataFrame()

# --- Pydantic Models ---

class PredictionRequest(BaseModel):
    # Flexible input based on what frontend sends
    features: List[dict]

class SimulationRequest(BaseModel):
    threshold: float
    cost_fn: float
    cost_fp: float

# --- API Endpoints ---

@app.get("/api/data/sample")
def get_data_sample():
    if DATA_SAMPLE.empty:
        return {"error": "Data not available"}
    # Convert to records
    return DATA_SAMPLE.to_dict(orient="records")

@app.post("/api/predict")
def predict(req: PredictionRequest):
    try:
        probs = model_engine.predict(req.features)
        return {"probabilities": probs}
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/simulate")
def simulate(req: SimulationRequest):
    try:
        # 1. Run Impact Calculation
        impact = simulation_engine.run_simulation(req.threshold, req.cost_fn, req.cost_fp)
        
        # 2. Generate Trade-off Curves (Cost vs Threshold)
        curves = simulation_engine.generate_curves(req.cost_fn, req.cost_fp)
        
        return {
            "impact": impact,
            "curves": curves
        }
    except Exception as e:
        logger.error(f"Simulation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
def get_stats():
    # Use validation predictions to show "Current System Status" mock
    try:
        if simulation_engine.df is None:
            simulation_engine.load_data()
            
        stats = get_dashboard_stats(simulation_engine.df, cost_fn=50000, cost_fp=10000) # Default costs
        return stats
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return {"error": "Stats unavailable"}

# --- Static Files ---
# Serve frontend from ../frontend
import os
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
