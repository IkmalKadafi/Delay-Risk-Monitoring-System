# Feature List & Data Dictionary (Engineered)

**Project:** Large-Scale Last-Mile Delivery Analytics  
**Stage:** STAGE 2 - Feature Engineering  
**Version:** 1.0

This document outlines the features engineered for the delay prediction model. These features are derived from the raw LaDe dataset.

---

## 1. Temporal Features (Time-Based)

These features capture cyclical patterns in delivery demand and traffic conditions.

| Feature Name | Category | Type | Business Meaning | Availability |
| :--- | :--- | :--- | :--- | :--- |
| `created_hour` | Temporal | Int (0-23) | The hour of the day the order was placed. Proxy for traffic congestion and order volume. | Task Creation |
| `created_day_of_week` | Temporal | Int (0-6) | Day of the week (Mon=0, Sun=6). Captures weekday vs. weekend patterns. | Task Creation |
| `is_weekend` | Temporal | Binary | Flag indicating if the order is on a Saturday or Sunday. | Task Creation |
| `is_peak_hour` | Temporal | Binary | Flag for high-traffic hours (e.g., 08:00-10:00, 17:00-19:00). | Task Creation |
| `created_hour_sin` / `_cos` | Temporal | Float | Cyclic encoding of the hour to preserve continuity between 23:00 and 00:00. | Task Creation |

---

## 2. Operational Features (Process-Based)

These features reflect the state of the logistics network and the specific task complexity.

| Feature Name | Category | Type | Business Meaning | Availability |
| :--- | :--- | :--- | :--- | :--- |
| `assignment_latency` | Operational | Float (min) | Time difference between `task_created` and `courier_assigned`. High latency implies driver shortage. | Courier Assignment |
| `pickup_distance_km` | Operational | Float | Estimated distance from courier's location at assignment to the pickup point. | Courier Assignment |
| `delivery_distance_km` | Operational | Float | Estimated distance from pickup point to delivery destination. | Task Creation |
| `order_volume_last_hour` | Contextual | Int | Number of orders created in the same city in the last hour. Proxy for system load. | Task Creation |

---

## 3. Geographic Features

| Feature Name | Category | Type | Business Meaning | Availability |
| :--- | :--- | :--- | :--- | :--- |
| `city_tier` | Geographic | Cat | Categorization of city (Tier 1, 2, 3) based on logistics maturity. | Task Creation |
| `pickup_cluster_id` | Geographic | Int | K-means cluster ID of the pickup location. Identifies high-volume merchant zones. | Task Creation |
| `dest_cluster_id` | Geographic | Int | K-means cluster ID of the destination. Identifies residential/commercial zones. | Task Creation |

---

## 4. Courier Historical Features (Advanced)

*Note: Calculated using a rolling window (e.g., last 7 days) excluding the current task to prevent leakage.*

| Feature Name | Category | Type | Business Meaning | Availability |
| :--- | :--- | :--- | :--- | :--- |
| `driver_avg_speed` | Historical | Float | The driver's average historical speed (km/h). | Courier Assignment |
| `driver_on_time_rate` | Historical | Float | Percentage of on-time deliveries by this driver in the last 7 days. | Courier Assignment |
| `driver_daily_load` | Historical | Int | Number of tasks already assigned to this driver today (prior to current task). | Courier Assignment |

---

## 5. Target Variable (Labels)

| Feature Name | Category | Type | Definition |
| :--- | :--- | :--- | :--- |
| `delivery_duration_min` | Target (Regression) | Float | `delivery_time` - `task_created_time` (in minutes). | Post-Delivery |
| `is_late` | Target (Class) | Binary | 1 if `delivery_duration_min` > SLA Threshold, else 0. | Post-Delivery |
