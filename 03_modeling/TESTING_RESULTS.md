# Modeling Scripts - Testing Results

**Project:** Large-Scale Last-Mile Delivery Analytics  
**Stage:** STAGE 3 - Predictive Modeling  
**Test Date:** January 17, 2026

---

## Test Summary

✅ **Status:** PASSED (All Scripts)  
✅ **Environment:** Dependencies (`xgboost`, `scikit-learn`) installed.  
✅ **Integration:** Model training -> saving -> evaluation -> explanation pipeline confirmed.

---

## Detailed Results

### 1. Training (`train_xgboost.py`)
*   **Result:** Success.
*   **Output:** `sla_risk_model.json` generated.
*   **Notes:** Demo data generation worked correctly. Training loop handled imbalance and completed.

### 2. Evaluation (`evaluate_model.py`)
*   **Result:** Success.
*   **Output:** operational metrics printed.
*   **Key Check:** Confusion Matrix and Recall calculation worked.

### 3. Risk Scoring (`risk_scoring.py`)
*   **Result:** Success.
*   **Output:** Correctly mapped probabilities (e.g., 0.85) to HIGH risk bands.

### 4. Feature Importance (`feature_importance.py`)
*   **Result:** Success (after bug fix).
*   **Fix Applied:** Updated `model.booster` to `model.get_booster()` for compatibility.
*   **Output:** `feature_importance.csv` generated.

---

## Artifacts Verified
The following files are verified working:
*   [x] `sla_risk_model.json` (Model Binary)
*   [x] `model_features.pkl` (Feature List)
*   [x] `feature_importance.csv` (Explainability Report)

**STAGE 3 is Verified Ready.**
