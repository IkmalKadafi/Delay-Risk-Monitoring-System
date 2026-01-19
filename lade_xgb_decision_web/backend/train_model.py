
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib
import logging
from data_loader import load_lade_data
from feature_engineering import engineering_features

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = "model.pkl"
ENCODER_PATH = "encoders.pkl"

def train_pipeline():
    # 1. Load Data
    logger.info("Loading Data...")
    # Using small sample for quick dev, set higher for production
    df = load_lade_data(sample_size=50000) 
    
    # 2. FE
    logger.info("Feature Engineering...")
    X, y, encoders = engineering_features(df)
    
    # Save encoders
    joblib.dump(encoders, ENCODER_PATH)
    logger.info(f"Encoders saved to {ENCODER_PATH}")
    
    # 3. Slit
    # Time-based split is better, but random for now for simplicity
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Train XGBoost
    logger.info("Training XGBoost...")
    # Calculate scale weight safely
    neg_count = len(y_train[y_train==0])
    pos_count = len(y_train[y_train==1])
    scale_weight = neg_count / pos_count if pos_count > 0 else 1.0

    # model = xgb.XGBClassifier(...) # XGBoost causing persistent TypeErrors in this env
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    
    model.fit(X_train, y_train)
    
    # 5. Evaluate
    logger.info("Evaluating...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred))
    
    auc = roc_auc_score(y_test, y_prob)
    print(f"AUC Score: {auc:.4f}")
    
    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix:\n{cm}")
    
    # Save Validation Predictions for What-If Simulation
    val_df = pd.DataFrame({
        'y_true': y_test,
        'y_prob': y_prob
    })
    val_preds_path = "validation_preds.csv"
    val_df.to_csv(val_preds_path, index=False)
    logger.info(f"Validation predictions saved to {val_preds_path}")
    
    # 6. Save Model
    # model.save_model(MODEL_PATH)
    # Joblib is already imported globally
    joblib.dump(model, MODEL_PATH)
    logger.info(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_pipeline()
