# Data Dictionary - LaDe Dataset

**Project:** Large-Scale Last-Mile Delivery Analytics untuk Optimasi SLA & Operasional Logistik  
**Stage:** STAGE 1 - Data Foundation & Problem Definition  
**Dataset Source:** Hugging Face (Cainiao-AI/LaDe)  
**Document Version:** 1.0  
**Last Updated:** January 2026

---

## Purpose

This data dictionary provides a comprehensive reference for all fields in the LaDe dataset, including raw fields from the source data and derived fields created during data preprocessing and feature engineering.

---

## Field Categories

Fields are organized into the following categories:
1. **Identifiers** - Unique keys for tasks, couriers, and events
2. **Temporal Fields** - Timestamps marking delivery lifecycle milestones
3. **Geographic Fields** - Location and routing information
4. **Event Fields** - Event types and status information
5. **Derived Fields** - Calculated metrics for SLA and analytics
6. **Target Labels** - Supervised learning labels

---

## 1. Identifiers

| Field Name | Description | Data Type | Source | Example Value | Nullability |
|------------|-------------|-----------|--------|---------------|-------------|
| `task_id` | Unique identifier for each delivery task. Primary key for grouping events and tracking task lifecycle. | String / Integer | Raw | `TASK_20260117_001234` | Not Null |
| `courier_id` | Unique identifier for each courier. Used for courier performance analysis and workload distribution. | String / Integer | Raw | `COURIER_5678` | Not Null |
| `event_id` | Unique identifier for each event within a task. Enables event-level tracking and sequencing. | String / Integer | Raw | `EVT_987654321` | Nullable |
| `city` | City or metropolitan area where the delivery occurs. Used for geographic segmentation and regional SLA analysis. | String (Categorical) | Raw | `Jakarta`, `Surabaya`, `Bandung` | Not Null |

---

## 2. Temporal Fields

| Field Name | Description | Data Type | Source | Example Value | Nullability |
|------------|-------------|-----------|--------|---------------|-------------|
| `task_created_time` | Timestamp when the delivery task was created in the system. Marks the start of the SLA measurement window. | Datetime | Raw | `2026-01-17 08:30:00` | Not Null |
| `task_assigned_time` | Timestamp when the task was assigned to a courier. Indicates dispatch efficiency. | Datetime | Raw | `2026-01-17 08:35:00` | Nullable |
| `pickup_time` | Timestamp when the courier picked up the package from the distribution center or merchant. Marks the beginning of active delivery. | Datetime | Raw | `2026-01-17 09:00:00` | Nullable |
| `delivery_time` | Timestamp when the package was successfully delivered to the customer. Marks the end of the SLA measurement window. | Datetime | Raw | `2026-01-17 10:15:00` | Nullable |
| `event_timestamp` | Timestamp of each individual event in the delivery lifecycle. Used for event sequencing and duration analysis. | Datetime | Raw | `2026-01-17 09:45:00` | Not Null |
| `first_attempt_time` | Timestamp of the first delivery attempt (if multiple attempts occur). | Datetime | Raw | `2026-01-17 10:00:00` | Nullable |
| `final_status_time` | Timestamp when the task reached a final status (delivered, failed, or cancelled). | Datetime | Raw | `2026-01-17 10:15:00` | Nullable |

---

## 3. Geographic Fields

| Field Name | Description | Data Type | Source | Example Value | Nullability |
|------------|-------------|-----------|--------|---------------|-------------|
| `city` | City or metropolitan area (also listed in Identifiers). | String (Categorical) | Raw | `Jakarta` | Not Null |
| `origin_lat` | Latitude of the pickup location (distribution center or merchant). | Float | Raw | `-6.2088` | Nullable |
| `origin_lon` | Longitude of the pickup location. | Float | Raw | `106.8456` | Nullable |
| `destination_lat` | Latitude of the delivery destination (customer address). | Float | Raw | `-6.1751` | Nullable |
| `destination_lon` | Longitude of the delivery destination. | Float | Raw | `106.8650` | Nullable |
| `distance_km` | Estimated or actual distance between origin and destination in kilometers. | Float | Raw / Derived | `5.2` | Nullable |
| `zone` | Delivery zone or district within the city (if available). | String (Categorical) | Raw | `Zone_A`, `Central` | Nullable |

---

## 4. Event Fields

| Field Name | Description | Data Type | Source | Example Value | Nullability |
|------------|-------------|-----------|--------|---------------|-------------|
| `event_type` | Type of event in the delivery lifecycle (e.g., `assigned`, `picked_up`, `in_transit`, `delivered`, `failed`). | String (Categorical) | Raw | `delivered`, `picked_up` | Not Null |
| `event_status` | Status or outcome of the event (e.g., `success`, `failure`, `pending`). | String (Categorical) | Raw | `success`, `customer_unavailable` | Nullable |
| `event_sequence` | Sequential order of the event within the task (1st event, 2nd event, etc.). | Integer | Derived | `1`, `2`, `3` | Not Null |
| `delivery_attempt_count` | Number of delivery attempts made for the task. | Integer | Derived | `1`, `2`, `3` | Nullable |
| `failure_reason` | Reason for delivery failure (if applicable). | String (Categorical) | Raw | `customer_unavailable`, `wrong_address` | Nullable |

---

## 5. Derived Fields (Calculated Metrics)

| Field Name | Description | Data Type | Source | Example Value | Nullability |
|------------|-------------|-----------|--------|---------------|-------------|
| `delivery_duration_minutes` | Total time elapsed from task creation to successful delivery, measured in minutes. **Primary SLA metric.** Formula: `(delivery_time - task_created_time)` in minutes. | Float | Derived | `105.0` (1 hour 45 minutes) | Nullable |
| `assignment_delay_minutes` | Time elapsed from task creation to courier assignment, in minutes. Formula: `(task_assigned_time - task_created_time)` in minutes. | Float | Derived | `5.0` | Nullable |
| `pickup_delay_minutes` | Time elapsed from task assignment to package pickup, in minutes. Formula: `(pickup_time - task_assigned_time)` in minutes. | Float | Derived | `25.0` | Nullable |
| `active_delivery_duration_minutes` | Time elapsed from pickup to successful delivery, in minutes. Formula: `(delivery_time - pickup_time)` in minutes. | Float | Derived | `75.0` | Nullable |
| `hour_of_day` | Hour of the day when the task was created (0-23). Used for temporal feature engineering. | Integer | Derived | `8`, `14`, `20` | Not Null |
| `day_of_week` | Day of the week when the task was created (0=Monday, 6=Sunday). Used for temporal feature engineering. | Integer | Derived | `0` (Monday), `5` (Saturday) | Not Null |
| `is_weekend` | Binary flag indicating whether the task was created on a weekend (Saturday or Sunday). | Integer (0/1) | Derived | `0` (weekday), `1` (weekend) | Not Null |
| `is_peak_hour` | Binary flag indicating whether the task was created during peak delivery hours (e.g., 11 AM - 2 PM, 6 PM - 9 PM). | Integer (0/1) | Derived | `0` (off-peak), `1` (peak) | Not Null |

---

## 6. Target Labels (Supervised Learning)

| Field Name | Description | Data Type | Source | Example Value | Nullability |
|------------|-------------|-----------|--------|---------------|-------------|
| `late` | **Binary SLA label.** Indicates whether the delivery violated the SLA threshold. Formula: `1` if `delivery_duration_minutes > SLA_threshold`, else `0`. | Integer (0/1) | Derived | `0` (on-time), `1` (late) | Not Null |
| `sla_threshold_minutes` | SLA threshold used for labeling (business-defined or data-driven). | Float | Derived | `120.0` (2 hours) | Not Null |
| `delay_severity` | Categorical label indicating severity of delay (optional, for multi-class classification). Values: `on_time`, `slightly_late`, `very_late`. | String (Categorical) | Derived | `on_time`, `very_late` | Nullable |

---

## 7. Additional Metadata Fields (Optional)

| Field Name | Description | Data Type | Source | Example Value | Nullability |
|------------|-------------|-----------|--------|---------------|-------------|
| `package_weight_kg` | Weight of the package in kilograms (if available). | Float | Raw | `2.5` | Nullable |
| `package_type` | Type of package (e.g., `document`, `parcel`, `food`). | String (Categorical) | Raw | `parcel`, `food` | Nullable |
| `service_type` | Type of delivery service (e.g., `express`, `same_day`, `next_day`). | String (Categorical) | Raw | `express`, `same_day` | Nullable |
| `weather_condition` | Weather condition at the time of delivery (if available). | String (Categorical) | Raw | `clear`, `rainy`, `heavy_traffic` | Nullable |
| `courier_experience_days` | Number of days the courier has been active in the system (tenure). | Integer | Derived | `120`, `365` | Nullable |
| `courier_avg_delivery_time` | Average delivery duration for the courier (historical performance metric). | Float | Derived | `95.5` | Nullable |

---

## 8. Data Quality Notes

### 8.1 Nullability Considerations
- **Critical Fields:** `task_id`, `courier_id`, `city`, `task_created_time`, `event_timestamp`, `event_type` should have minimal null values.
- **Nullable Fields:** Intermediate timestamps (`task_assigned_time`, `pickup_time`) may be null if events were not recorded or if the task was cancelled before reaching that stage.
- **Derived Fields:** Nullability depends on the availability of raw fields. For example, `delivery_duration_minutes` will be null if `delivery_time` is null.

### 8.2 Data Type Assumptions
- **Datetime Fields:** Assumed to be in UTC or local timezone (verify during data ingestion).
- **Categorical Fields:** May require encoding (one-hot, label encoding) for machine learning models.
- **Numeric Fields:** Should be validated for outliers and extreme values (e.g., negative durations, unrealistic distances).

### 8.3 Data Validation Rules
- `delivery_duration_minutes` must be ≥ 0 (non-negative)
- `event_sequence` must be sequential and unique within a task
- `delivery_time` must be ≥ `task_created_time` (temporal consistency)
- `distance_km` must be ≥ 0 (non-negative)

---

## 9. Usage in Analytics Pipeline

### 9.1 Feature Engineering
- **Temporal Features:** Extract `hour_of_day`, `day_of_week`, `is_weekend`, `is_peak_hour` from `task_created_time`
- **Geographic Features:** Calculate `distance_km` from lat/lon coordinates; aggregate city-level statistics
- **Courier Features:** Compute courier-level aggregations (average delivery time, task count, SLA violation rate)
- **Event Features:** Count events per task, calculate time between events, identify event patterns

### 9.2 SLA Labeling
- Use `delivery_duration_minutes` and `sla_threshold_minutes` to generate the `late` label
- Validate label distribution and class balance before modeling

### 9.3 Model Training
- **Input Features:** Temporal, geographic, courier, and event-based features
- **Target Variable:** `late` (binary classification)
- **Evaluation Metrics:** Precision, Recall, F1-Score, AUC-ROC

---

## 10. Document Governance

**Maintained By:** Data Engineering & Data Science Teams  
**Review Cycle:** Updated as new fields are added or schema changes occur  
**Version Control:** Track changes in version history

**Related Documents:**
- `data_schema.md`: High-level schema overview and delivery lifecycle
- `sla_definition.md`: SLA metric definition and labeling strategy

---

**Document Owner:** Entropiata Agency
**Approved By:** [Business Manager]
**Last Reviewed:** January 2026
