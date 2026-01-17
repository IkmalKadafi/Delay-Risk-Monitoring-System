# Model Card: SLA Risk Predictor (XGBoost)

**Model Version:** 1.0  
**Date:** January 2026  
**Type:** Binary Classification (Supervised Learning)  
**Author:** Data Science Team

---

## 1. Problem Definition
*   **Goal:** Predict the likelihood of a last-mile delivery task breaching its Service Level Agreement (SLA) (e.g., > 120 mins).
*   **Business Impact:** Enable dispatchers to proactively intervene on high-risk orders *before* the delay occurs, reducing "Late Data" penalties and improving customer satisfaction.
*   **Input:** Task attributes (time, location, courier history) known at time of creation/assignment.
*   **Output:** Probability (0-1) of class `Late`.

---

## 2. Intended Use
*   **Primary User:** Logistics Operations Team / Automated Dispatch System.
*   **Usage Scenario:** Real-time scoring of new orders. High-risk orders trigger alerts on the dashboard.
*   **Out of Scope:**
    *   Dynamic route optimization (this model predicts risk, it doesn't solve TSP).
    *   Courier fraud detection.

---

## 3. Training Data
*   **Dataset:** LaDe (Last-mile Delivery Dataset) - Offline preparation.
*   **Timeframe:** [Insert Date Range]
*   **Grain:** 1 row per delivery task.
*   **Preprocessing:**
    *   Temporal cyclical encoding.
    *   Missing values handled by XGBoost default.
    *   Class imbalance handled via `scale_pos_weight`.

---

## 4. Model Details
*   **Architecture:** XGBoost (Gradient Boosted Decision Trees).
*   **Objective:** Binary Logistic.
*   **Evaluation Metric:** ROC-AUC (Primary), Recall @ Class 1 (Operational).
*   **Key Parameters:**
    *   `scale_pos_weight`: Dynamic based on training set imbalance.
    *   `max_depth`: 5 (Restricted complexity).
    *   `learning_rate`: 0.05.

---

## 5. Performance & Limitations
*   **Metrics (Validation):**
    *   Expected AUC: > 0.75 (Baseline).
    *   Recall (Late): Target > 70%.
*   **Limitations:**
    *   **Cold Start:** New couriers with no history will have imputed average stats, reducing prediction accuracy for their tasks.
    *   **External Force Majeure:** Cannot predict delays due to sudden unmapped road closures or extreme weather events unless weather data is explicitly joined.
*   **Bias Considerations:**
    *   **Geographic:** Rural areas might have higher baseline risk; ensure model isn't just learning "Rural = Late".
    *   **Courier Tenure:** Model penalizes couriers with poor history; operational protocols should use this for *support*, not punitive automated firing.

---

## 6. Operational Risk
*   **False Positive (False Alarm):** Operations team wastes time checking an on-time order. Cost = Low (Minutes of labor).
*   **False Negative (Missed Delay):** Order is late without warning. Customer churns. Cost = High ($$$).
*   **Mitigation:** The decision threshold is tuned to favor Recall (catching delays) over Precision.
