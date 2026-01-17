"""
Decision Engine (Business Logic)
================================

Purpose:
    - The "Brain" of the operation.
    - Takes a raw risk score.
    - Applies Business Rules (Alert Policy).
    - Outputs the Final Decision/Action.

Author: Decision Science Team
Stage: STAGE 4 - Real-Time System
"""

class DecisionEngine:
    def __init__(self):
        # Thresholds defined in Alert Policy
        # In production, fetch these from a dynamic config service
        self.thresholds = {
            'HIGH': 0.70,   # > 70% chance of late
            'MEDIUM': 0.40  # > 40% chance
        }
    
    def evaluate_risk(self, task_id, risk_probability, context=None):
        """
        Determines the operational action based on risk score.
        """
        decision_record = {
            "task_id": task_id,
            "risk_prob": risk_probability,
            "timestamp": context.get('timestamp') if context else None
        }
        
        if risk_probability >= self.thresholds['HIGH']:
            decision_record.update({
                "level": "CRITICAL",
                "action_code": "ACT_001",
                "action_desc": "IMMEDIATE INTERVENTION",
                "message": f"High risk of SLA breach ({risk_probability:.2%}). Re-route or escalate."
            })
            
        elif risk_probability >= self.thresholds['MEDIUM']:
            decision_record.update({
                "level": "WARNING",
                "action_code": "ACT_002",
                "action_desc": "MONITOR",
                "message": "Potential delay. Add to dispatcher watchlist."
            })
            
        else:
            decision_record.update({
                "level": "NORMAL",
                "action_code": "ACT_000",
                "action_desc": "NO ACTION",
                "message": "On track."
            })
            
        return decision_record

# Unit Test
if __name__ == "__main__":
    engine = DecisionEngine()
    print(engine.evaluate_risk("T100", 0.85))
    print(engine.evaluate_risk("T101", 0.45))
    print(engine.evaluate_risk("T102", 0.10))
