
import pandas as pd
import numpy as np
from cost_evaluation import calculate_financial_impact

def get_dashboard_stats(predictions_df, cost_fn, cost_fp):
    """
    Computes high-level stats for the dashboard.
    Args:
        predictions_df (pd.DataFrame): Must contain 'y_prob' and 'sla_breach' (if available).
        cost_fn, cost_fp: Costs.
    Returns:
        dict: Aggregated stats.
    """
    total_deliveries = len(predictions_df)
    
    # Assume default threshold 0.5 for dashboard view
    threshold = 0.5
    y_prob = predictions_df['y_prob']
    y_pred = (y_prob >= threshold).astype(int)
    
    risk_exposure = np.sum(y_prob * cost_fn)
    
    high_risk_count = np.sum(y_prob >= 0.7)
    medium_risk_count = np.sum((y_prob >= 0.3) & (y_prob < 0.7))
    low_risk_count = np.sum(y_prob < 0.3)
    
    predicted_breaches = np.sum(y_pred)
    
    return {
        "total_deliveries": int(total_deliveries),
        "predicted_breaches": int(predicted_breaches),
        "breach_rate": float(predicted_breaches / total_deliveries if total_deliveries > 0 else 0),
        "total_risk_exposure": float(risk_exposure),
        "risk_distribution": {
            "high": int(high_risk_count),
            "medium": int(medium_risk_count),
            "low": int(low_risk_count)
        }
    }
