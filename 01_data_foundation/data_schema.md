# LaDe Dataset Schema Documentation

**Project:** Large-Scale Last-Mile Delivery Analytics untuk Optimasi SLA & Operasional Logistik  
**Stage:** STAGE 1 - Data Foundation & Problem Definition  
**Dataset Source:** Hugging Face (Cainiao-AI/LaDe)  
**Document Version:** 1.0  
**Last Updated:** January 2026

---

## Executive Summary

The LaDe (Last-mile Delivery) dataset is a large-scale, real-world dataset containing event-based delivery data from last-mile logistics operations. This document provides a comprehensive overview of the dataset structure, key identifiers, temporal fields, and the delivery lifecycle represented in the data.

---

## 1. Dataset Overview

### 1.1 Data Nature
- **Type:** Event-based, time-series delivery data
- **Scale:** Large-scale (enterprise-grade)
- **Domain:** Last-mile logistics and delivery operations
- **Granularity:** Individual delivery events tracked at the task level

### 1.2 Core Entities

The LaDe dataset is structured around two fundamental entities:

#### **Delivery Task**
A delivery task represents a complete delivery assignment from pickup to final delivery. Each task is uniquely identified and contains:
- A specific origin (pickup location)
- A specific destination (delivery location)
- An assigned courier
- A defined time window or expected delivery timeframe
- A sequence of events that track the task's progression

**Business Definition:**  
A delivery task is the atomic unit of work in last-mile logistics. It represents one courier's responsibility to transport one or more packages from a distribution center or merchant to an end customer.

#### **Event**
An event represents a specific state change or milestone in the delivery lifecycle. Events are timestamped actions that occur during task execution, such as:
- Task assignment to courier
- Pickup confirmation
- In-transit status updates
- Delivery attempts
- Successful delivery or failure

**Business Definition:**  
Events are the building blocks of delivery tracking. They provide granular visibility into the delivery process, enabling SLA monitoring, operational analysis, and predictive modeling.

---

## 2. Key Identifiers

The following identifiers are critical for data analysis and modeling:

| Identifier | Description | Uniqueness | Business Purpose |
|------------|-------------|------------|------------------|
| `task_id` | Unique identifier for each delivery task | Unique per task | Primary key for delivery tasks; used to group events and track task lifecycle |
| `courier_id` | Unique identifier for each courier | Unique per courier | Enables courier performance analysis, workload distribution, and behavioral modeling |
| `city` | City or metropolitan area where delivery occurs | Non-unique (categorical) | Geographic segmentation for regional SLA analysis and operational optimization |
| `event_id` | Unique identifier for each event (if available) | Unique per event | Enables event-level tracking and sequencing |

### Identifier Relationships
- **One-to-Many:** One `task_id` can have multiple events (task lifecycle)
- **One-to-Many:** One `courier_id` can be associated with multiple tasks (courier workload)
- **Many-to-One:** Multiple tasks can occur in the same `city` (geographic clustering)

---

## 3. Temporal Fields

Timestamps are critical for SLA calculation, delay prediction, and operational analytics. The LaDe dataset contains several timestamp fields that mark key milestones in the delivery lifecycle.

### 3.1 Core Timestamp Fields

| Timestamp Field | Business Meaning | SLA Relevance |
|-----------------|------------------|---------------|
| `task_created_time` | When the delivery task was created in the system | Start of SLA measurement window |
| `task_assigned_time` | When the task was assigned to a courier | Indicates dispatch efficiency |
| `pickup_time` | When the courier picked up the package | Marks beginning of active delivery |
| `delivery_time` | When the package was successfully delivered | End of SLA measurement window |
| `event_timestamp` | Timestamp of each individual event | Enables event sequencing and duration analysis |

### 3.2 Derived Temporal Metrics

From these timestamps, we can derive critical business metrics:

- **Assignment Delay:** `task_assigned_time - task_created_time`
- **Pickup Delay:** `pickup_time - task_assigned_time`
- **Delivery Duration:** `delivery_time - pickup_time`
- **Total Task Duration:** `delivery_time - task_created_time` *(Primary SLA metric)*

---

## 4. Delivery Lifecycle

Events in the LaDe dataset form a structured lifecycle that represents the progression of a delivery task from creation to completion (or failure).

### 4.1 Standard Delivery Lifecycle

```
┌─────────────────┐
│  Task Created   │ ← task_created_time
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Task Assigned   │ ← task_assigned_time
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Pickup Event   │ ← pickup_time
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  In-Transit     │ ← Multiple status events
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Delivery Event  │ ← delivery_time
└─────────────────┘
```

### 4.2 Event Sequencing

Events are ordered chronologically by `event_timestamp`. The sequence of events provides:
- **Operational visibility:** Track where delays occur in the delivery process
- **Behavioral patterns:** Identify common courier behaviors or bottlenecks
- **Anomaly detection:** Detect unusual event sequences that may indicate issues

### 4.3 Lifecycle Variations

Not all deliveries follow the standard lifecycle. Common variations include:
- **Failed deliveries:** Task ends with a failure event (customer unavailable, wrong address, etc.)
- **Multiple delivery attempts:** Task has multiple delivery events before success
- **Cancelled tasks:** Task is cancelled before completion
- **Returned packages:** Task includes return-to-sender events

These variations are critical for comprehensive SLA analysis and operational optimization.

---

## 5. Data Characteristics

### 5.1 Event-Based Structure
- Each row in the dataset typically represents an **event**, not a complete task
- Tasks are reconstructed by grouping events by `task_id`
- Event ordering is determined by `event_timestamp`

### 5.2 Temporal Ordering
- Events within a task must be sorted by timestamp for accurate lifecycle analysis
- Out-of-order events may indicate data quality issues or system delays

### 5.3 Completeness Considerations
- Some tasks may have incomplete event sequences (missing events)
- Timestamp fields may be null for certain event types
- Data quality validation is essential before SLA calculation

---

## 6. Schema Usage in Analytics Pipeline

This schema understanding enables:

1. **SLA Definition:** Use `task_created_time` and `delivery_time` to calculate delivery duration and label tasks as on-time or late

2. **Feature Engineering:** Extract temporal features (hour of day, day of week), geographic features (city-level aggregations), and courier features (historical performance)

3. **Delay Prediction:** Use event sequences and timestamps to predict whether a task will violate SLA before completion

4. **Operational Optimization:** Identify bottlenecks in the delivery lifecycle and optimize courier assignment, routing, and scheduling

---

## 7. Next Steps

After understanding this schema:
1. Review `sla_definition.md` to understand how SLA labels are derived from these timestamps
2. Review `data_dictionary.md` for a complete field-level reference
3. Execute `data_ingestion.py` to explore actual data samples and validate schema understanding

---

**Document Owner:** Entropiata Agency  
**Review Cycle:** Quarterly or upon schema changes  
**Related Documents:** `sla_definition.md`, `data_dictionary.md`
