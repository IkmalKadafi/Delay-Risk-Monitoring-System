"""
Risk Scoring & Operational Bands
================================

Purpose:
    - Convert raw model probabilities (0.0 - 1.0) into actionable Risk Categories.
    - Define clear protocols for each risk level.
    
Usage:
    - This module is used during Inference.
    - It maps Probability -> Score -> Action.

Author: Decision Science Team
Stage: STAGE 3 - Risk Scoring
"""

def calculate_risk_score(probability):
    """
    Convert probability to a user-friendly score (0-100).
    """
    return int(round(probability * 100))

def determine_risk_band(probability, thresholds=None):
    """
    Map probability to Risk Level.
    
    Default Thresholds:
    - Low Risk:    0.00 - 0.40  (Unlikely to be late)
    - Medium Risk: 0.40 - 0.70  (Potential delay, monitor)
    - High Risk:   0.70 - 1.00  (Critical, intervene immediately)
    
    Args:
        probability (float): Model output (0-1).
        thresholds (dict): Optional custom thresholds.
        
    Returns:
        tuple: (Risk Label, Action Code)
    """
    if thresholds is None:
        thresholds = {'medium': 0.40, 'high': 0.70}
        
    if probability < thresholds['medium']:
        return "LOW", "NO_ACTION"
    elif probability < thresholds['high']:
        return "MEDIUM", "MONITOR_DASHBOARD"
    else:
        return "HIGH", "TRIGGER_ALERT"

def simulated_inference_pipeline(task_features, model):
    """
    Simulates the end-to-end scoring process for a single task.
    """
    # 1. Get raw probability
    # Assuming task_features is reshaped for model input
    prob = model.predict_proba(task_features)[0][1]
    
    # 2. Get Score
    score = calculate_risk_score(prob)
    
    # 3. Get Band
    band, action = determine_risk_band(prob)
    
    return {
        "risk_probability": round(prob, 4),
        "risk_score": score,
        "risk_level": band,
        "recommended_action": action
    }

# Example Operational Protocol Documentation (Embedded)
OPERATIONAL_PROTOCOLS = {
    "LOW": "Standard routing. No manual check required.",
    "MEDIUM": "Flag on dispatcher dashboard. Auto-message driver to check status.",
    "HIGH": "CRITICAL ALERT. Dispatcher must call driver or re-assign standard orders to free up capacity."
}

if __name__ == "__main__":
    # Test the logic with mock probabilities
    test_probs = [0.15, 0.55, 0.85]
    print("Risk Scoring System Test:")
    print("-" * 50)
    print(f"{'Prob':<10} | {'Score':<5} | {'Risk Band':<10} | {'Action':<20}")
    print("-" * 50)
    
    for p in test_probs:
        band, action = determine_risk_band(p)
        score = calculate_risk_score(p)
        print(f"{p:<10} | {score:<5} | {band:<10} | {action:<20}")
