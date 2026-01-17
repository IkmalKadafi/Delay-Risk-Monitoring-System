
import numpy as np

def calculate_financial_impact(y_true, y_prob, threshold, cost_fn, cost_fp):
    """
    Calculates the financial impact of a decision threshold.
    
    Args:
        y_true (array-like): True labels (0 or 1).
        y_prob (array-like): Predicted probabilities.
        threshold (float): Decision threshold.
        cost_fn (float): Cost of a False Negative (Missed SLA).
        cost_fp (float): Cost of a False Positive (Unnecessary Intervention).
        
    Returns:
        dict: Financial metrics.
    """
    y_pred = (y_prob >= threshold).astype(int)
    
    # Confusion Matrix Components
    tp = np.sum((y_pred == 1) & (y_true == 1))
    fp = np.sum((y_pred == 1) & (y_true == 0))
    tn = np.sum((y_pred == 0) & (y_true == 0))
    fn = np.sum((y_pred == 0) & (y_true == 1))
    
    # Financial Calculation
    total_cost_fn = fn * cost_fn
    total_cost_fp = fp * cost_fp
    total_risk_cost = total_cost_fn + total_cost_fp
    
    intervention_count = tp + fp
    missed_count = fn
    
    return {
        "threshold": threshold,
        "total_cost": total_risk_cost,
        "cost_fn_total": total_cost_fn,
        "cost_fp_total": total_cost_fp,
        "intervention_count": int(intervention_count),
        "missed_sla_count": int(missed_count),
        "fp_count": int(fp),
        "fn_count": int(fn),
        "tp_count": int(tp),
        "tn_count": int(tn)
    }

def estimate_risk_exposure(y_prob, cost_fn):
    """
    Estimates total risk exposure if NO action is taken.
    Risk = Sum(Probability of Breach * Cost of Breach)
    """
    return np.sum(y_prob * cost_fn)
