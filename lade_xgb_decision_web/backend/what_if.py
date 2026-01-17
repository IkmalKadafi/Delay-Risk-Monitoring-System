
import pandas as pd
import numpy as np
from cost_evaluation import calculate_financial_impact, estimate_risk_exposure
import logging

logger = logging.getLogger(__name__)

class SimulationEngine:
    def __init__(self, validation_data_path="validation_preds.csv"):
        # We assume validation data (X, y_true, y_prob) is saved after training
        # If not, we might need to load valid set and predict once.
        self.data_path = validation_data_path
        self.df = None
        
    def load_data(self):
        if self.df is None:
            # For now, we mock or load. Real impl should save validation probs during training.
            # Let's assume train_model.py saves a 'validation_preds.csv' with columns: [true_label, prob]
            try:
                self.df = pd.read_csv(self.data_path)
            except:
                logger.warning("Validation predictions not found. Using mock data for simulation test.")
                self.df = pd.DataFrame({
                    'y_true': np.random.randint(0, 2, 1000),
                    'y_prob': np.random.uniform(0, 1, 1000)
                })

    def run_simulation(self, threshold, cost_fn, cost_fp):
        self.load_data()
        
        y_true = self.df['y_true'].values
        y_prob = self.df['y_prob'].values
        
        impact = calculate_financial_impact(y_true, y_prob, threshold, cost_fn, cost_fp)
        
        # Calculate Baseline (Static Threshold 0.5 like standard model)
        baseline = calculate_financial_impact(y_true, y_prob, 0.5, cost_fn, cost_fp)
        
        impact['savings_vs_baseline'] = baseline['total_cost'] - impact['total_cost']
        
        return impact

    def generate_curves(self, cost_fn, cost_fp, points=20):
        self.load_data()
        thresholds = np.linspace(0.01, 0.99, points)
        results = []
        for t in thresholds:
            res = calculate_financial_impact(self.df['y_true'].values, self.df['y_prob'].values, t, cost_fn, cost_fp)
            results.append({
                "threshold": t,
                "total_cost": res['total_cost'],
                "intervention_rate": res['intervention_count'] / len(self.df)
            })
        return results

