# Offline Dataset Specification (Modeling Table)

**Project:** Large-Scale Last-Mile Delivery Analytics  
**Stage:** STAGE 2 - Dataset Preparation

This document defines the schema and logic for the final "Gold" dataset used for model training and validation.

---

## 1. Dataset Overview

*   **Dataset Name:** `training_set_v1.parquet`
*   **Grain:** One row per unique `task_id`.
*   **Timeframe:** Historical data (e.g., Jan 2023 - Dec 2023).
*   **Purpose:** Train XGBoost/LightGBM classification models for SLA breach prediction.

---

## 2. Table Schema

The final table will contain the following column groups:

### A. Identifiers (Metadata)
*These columns are for tracking and joining, NOT for training.*
*   `task_id` (String)
*   `courier_id` (String)
*   `city_code` (String)
*   `partition_date` (Date) - For data partitioning.

### B. Input Features (X)
*Columns used by the model for prediction.*

**1. Temporal**
*   `created_hour_sin` (Float)
*   `created_hour_cos` (Float)
*   `is_weekend` (Int 0/1)
*   `is_holiday` (Int 0/1)

**2. Geographic & Trip**
*   `delivery_distance_km` (Float) - *Estimated at assignment time*
*   `pickup_cluster` (Category/Int)
*   `dest_cluster` (Category/Int)

**3. Operational Context (Point-in-Time)**
*   `order_volume_last_1h` (Int) - *Volume in the city at creation time*
*   `active_couriers_in_zone` (Int) - *Supply availability*

**4. Courier History (Point-in-Time)**
*   `courier_avg_speed_7d` (Float)
*   `courier_late_rate_7d` (Float)

### C. Target Variables (y)
*   `delivery_duration_actual` (Float) - *Ground Truth*
*   `is_late` (Int 0/1) - *Target Label*

---

## 3. Leakage Prevention Strategy (Critical)

To simulate a real-time production environment, strictly observe the following rules during dataset construction:

1.  **Prediction Point:** The "moment of prediction" is defined as `task_created_time` or `courier_assigned_time`.
2.  **Future Data Exclusion:** Any data generated *after* the prediction point must be excluded from Input Features.
    *   *Examples of Leaks (DO NOT USE):* `delivery_time`, `signature_image_url`, `customer_rating`, `actual_traffic_during_trip`.
3.  **Historical Aggregates:** Features based on history (e.g., courier performance) must only use data from *before* the current task creation timestamp.

---

## 4. Sampling & Splitting

*   **Train/Val/Test Split:** MUST be Time-Based (not Random).
    *   *Train:* Jan - Sep
    *   *Validation:* Oct
    *   *Test:* Nov - Dec
    *   *Reason:* Delivery patterns are seasonal; random splitting leaks future trends into the past.
*   **Negative Sampling:** If `is_late` class is rare (<5%), preserve all positive cases and downsample negative cases to achieve a manageable ratio (e.g., 1:10) if dataset size is prohibitive.

---

## 5. Next Steps

1.  Run `feature_pipeline.py` on the full LaDe historical dump.
2.  Apply `labeling_logic.py` to generate `is_late` column.
3.  Save result as Parquet (columnar storage optimized for analytics).
4.  Proceed to STAGE 3 (Model Training).
