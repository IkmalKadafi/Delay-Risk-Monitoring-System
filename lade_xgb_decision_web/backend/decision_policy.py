
def apply_decision_policy(prob, t1=0.3, t2=0.7):
    """
    Applies the decision policy based on risk buckets.
    
    Args:
        prob (float): Probability of SLA breach.
        t1 (float): Threshold for Low/Medium risk.
        t2 (float): Threshold for Medium/High risk.
        
    Returns:
        dict: Decision details (Risk Level, Action, Color).
    """
    if prob < t1:
        return {
            "risk_level": "Low",
            "action": "Monitor",
            "color": "green",
            "description": "Standard tracking. No intervention needed."
        }
    elif prob < t2:
        return {
            "risk_level": "Medium",
            "action": "Prioritize",
            "color": "yellow",
            "description": "Flag for potential delay. Assign to priority queue."
        }
    else:
        return {
            "risk_level": "High",
            "action": "Escalate",
            "color": "red",
            "description": "Immediate intervention required. Notify ops manager."
        }
