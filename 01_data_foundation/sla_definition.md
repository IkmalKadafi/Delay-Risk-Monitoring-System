# SLA Definition & Labeling Strategy

**Project:** Large-Scale Last-Mile Delivery Analytics untuk Optimasi SLA & Operasional Logistik  
**Stage:** STAGE 1 - Data Foundation & Problem Definition  
**Document Version:** 1.0  
**Last Updated:** January 2026

---

## Executive Summary

This document defines the Service Level Agreement (SLA) metric and labeling strategy for the last-mile delivery analytics project. The SLA definition serves as the foundation for delay prediction modeling, operational performance monitoring, and business decision-making.

---

## 1. Business Definition of SLA

### 1.1 What is SLA in Last-Mile Delivery?

**Service Level Agreement (SLA)** in the context of last-mile delivery refers to the contractual or operational commitment to deliver packages within a specified timeframe.

**Business Context:**
- SLA is a critical performance indicator for logistics companies
- Meeting SLA targets directly impacts customer satisfaction, retention, and brand reputation
- SLA violations result in operational costs (refunds, re-delivery) and customer churn
- Predictive SLA monitoring enables proactive intervention to prevent delays

### 1.2 SLA Components

An SLA in last-mile delivery typically consists of:
1. **Start Time:** When the delivery commitment begins (e.g., task creation, pickup time)
2. **End Time:** When the delivery is completed (e.g., successful delivery timestamp)
3. **Threshold:** Maximum acceptable delivery duration (e.g., 2 hours, same-day, next-day)
4. **Measurement Unit:** Time unit for duration calculation (minutes, hours, days)

---

## 2. Mathematical Definition of Delivery Duration

### 2.1 Primary SLA Metric: Total Delivery Duration

For this project, we define **Delivery Duration** as the total time elapsed from task creation to successful delivery.

**Formula:**

```
Delivery_Duration = delivery_time - task_created_time
```

**Where:**
- `delivery_time`: Timestamp when the package was successfully delivered to the customer
- `task_created_time`: Timestamp when the delivery task was created in the system

**Unit:** Minutes (for granular analysis) or Hours (for business reporting)

### 2.2 Rationale for This Definition

**Why use `task_created_time` as the start point?**
- Represents the customer's expectation: from the moment the order is placed, the clock is ticking
- Captures the entire delivery process, including dispatch delays and courier assignment inefficiencies
- Aligns with customer-facing SLA commitments (e.g., "delivery within 2 hours of order placement")

**Why use `delivery_time` as the end point?**
- Marks the successful completion of the delivery task
- Represents the actual customer experience
- Excludes failed or cancelled deliveries from SLA calculation (these are handled separately)

### 2.3 Alternative Duration Metrics (Not Primary SLA)

While not used for primary SLA labeling, these metrics provide operational insights:

| Metric | Formula | Business Use Case |
|--------|---------|-------------------|
| **Assignment Delay** | `task_assigned_time - task_created_time` | Measures dispatch efficiency |
| **Pickup Delay** | `pickup_time - task_assigned_time` | Measures courier responsiveness |
| **Active Delivery Duration** | `delivery_time - pickup_time` | Measures actual transit time |

---

## 3. Binary SLA Label Definition

### 3.1 Label Definition

To enable supervised machine learning for delay prediction, we define a binary label:

**Label: `late`**

```
late = 1  if  Delivery_Duration > SLA_Threshold
late = 0  if  Delivery_Duration ≤ SLA_Threshold
```

**Where:**
- `late = 1`: SLA violation (delivery was late)
- `late = 0`: SLA met (delivery was on-time)
- `SLA_Threshold`: Maximum acceptable delivery duration (business-defined)

### 3.2 SLA Threshold Selection

The SLA threshold is a **business decision** that depends on:
- Service type (express delivery, same-day, next-day)
- Geographic region (urban vs. rural)
- Customer segment (premium vs. standard)
- Competitive benchmarks

**Example Thresholds:**
- **Express Delivery:** 2 hours
- **Same-Day Delivery:** 12 hours
- **Next-Day Delivery:** 24 hours

**For this project:**  
We will analyze the distribution of delivery durations in the LaDe dataset and define the threshold based on:
1. **Median or percentile-based approach:** e.g., 75th percentile of delivery durations
2. **Business-driven approach:** If domain knowledge suggests a specific threshold (e.g., 2 hours for urban deliveries)

> **Note:** The exact threshold will be determined during exploratory data analysis (EDA) in STAGE 2.

### 3.3 Labeling Logic (Pseudocode)

```python
def calculate_sla_label(task_created_time, delivery_time, sla_threshold_minutes):
    """
    Calculate binary SLA label for a delivery task.
    
    Args:
        task_created_time (datetime): When the task was created
        delivery_time (datetime): When the delivery was completed
        sla_threshold_minutes (int): SLA threshold in minutes
    
    Returns:
        int: 1 if late, 0 if on-time
    """
    # Calculate delivery duration in minutes
    delivery_duration = (delivery_time - task_created_time).total_seconds() / 60
    
    # Apply SLA threshold
    if delivery_duration > sla_threshold_minutes:
        return 1  # Late
    else:
        return 0  # On-time
```

---

## 4. Rationale for This SLA Definition

### 4.1 Why Binary Labeling?

**Advantages:**
- **Simplicity:** Clear, interpretable labels for business stakeholders
- **Actionability:** Binary classification aligns with operational decision-making (intervene or not)
- **Model Compatibility:** Supports standard classification algorithms (logistic regression, XGBoost, neural networks)

**Trade-offs:**
- Does not capture severity of delay (e.g., 5 minutes late vs. 2 hours late)
- May require threshold tuning to balance precision and recall

### 4.2 Why This Specific Duration Metric?

**Customer-Centric:**
- Reflects the customer's end-to-end experience
- Aligns with customer-facing SLA commitments

**Operationally Comprehensive:**
- Captures all phases of the delivery process (dispatch, pickup, transit, delivery)
- Enables identification of bottlenecks across the entire lifecycle

**Data Availability:**
- `task_created_time` and `delivery_time` are typically well-populated in delivery datasets
- Minimizes reliance on intermediate timestamps that may have missing values

---

## 5. Alternative SLA Definitions (Not Implemented)

For transparency and future consideration, we document alternative SLA definitions:

### 5.1 Multi-Class SLA Labels

Instead of binary labels, use multiple classes:
- **On-Time:** Delivery within SLA threshold
- **Slightly Late:** Delivery within 1.5x SLA threshold
- **Very Late:** Delivery beyond 1.5x SLA threshold

**Use Case:** When understanding delay severity is critical for prioritization

### 5.2 Regression-Based SLA Prediction

Instead of predicting binary labels, predict the exact delivery duration.

**Use Case:** When precise ETA (Estimated Time of Arrival) is needed for customer communication

### 5.3 Time-Window-Based SLA

Define SLA based on promised delivery time windows (e.g., "delivery between 2 PM - 4 PM").

**Use Case:** When delivery commitments are time-window-specific rather than duration-based

### 5.4 Geographic-Specific SLA Thresholds

Use different SLA thresholds for different cities or regions.

**Use Case:** When operational conditions vary significantly across geographies

---

## 6. SLA Labeling in the Analytics Pipeline

### 6.1 Data Preprocessing

1. **Filter Completed Deliveries:** Only include tasks with non-null `delivery_time` (exclude failed/cancelled tasks)
2. **Calculate Duration:** Compute `Delivery_Duration` for each task
3. **Apply Threshold:** Generate binary `late` label based on SLA threshold
4. **Validate Labels:** Check for data quality issues (negative durations, extreme outliers)

### 6.2 Label Distribution Analysis

Before modeling, analyze:
- **Class Balance:** Proportion of late vs. on-time deliveries
- **Temporal Patterns:** SLA violation rates by time of day, day of week
- **Geographic Patterns:** SLA violation rates by city
- **Courier Patterns:** SLA violation rates by courier

### 6.3 Handling Class Imbalance

If the dataset is imbalanced (e.g., 90% on-time, 10% late):
- Use stratified sampling for train/test splits
- Apply class weighting in model training
- Consider resampling techniques (SMOTE, undersampling)

---

## 7. Success Metrics for SLA Prediction

Once the SLA label is defined, model performance will be evaluated using:

| Metric | Definition | Business Relevance |
|--------|------------|-------------------|
| **Precision** | % of predicted late deliveries that are actually late | Minimizes false alarms (operational efficiency) |
| **Recall** | % of actual late deliveries that are correctly predicted | Maximizes detection of at-risk deliveries (customer satisfaction) |
| **F1-Score** | Harmonic mean of precision and recall | Balances false positives and false negatives |
| **AUC-ROC** | Area under ROC curve | Overall model discrimination ability |

**Business Priority:**  
High **Recall** is typically prioritized in SLA prediction to ensure most at-risk deliveries are flagged for intervention.

---

## 8. Next Steps

After defining the SLA metric:
1. Execute `data_ingestion.py` to load sample data
2. Perform exploratory data analysis (EDA) to determine optimal SLA threshold
3. Calculate and validate SLA labels on the LaDe dataset
4. Analyze label distribution and class balance
5. Proceed to STAGE 2: Feature Engineering & Model Development

---

## 9. Document Governance

**Decision Authority:** Product Owner, Data Science Lead  
**Review Cycle:** Quarterly or upon business requirement changes  
**Change Log:**
- v1.0 (January 2026): Initial SLA definition for project kickoff

**Related Documents:**
- `data_schema.md`: Dataset structure and timestamp definitions
- `data_dictionary.md`: Complete field reference

---

**Document Owner:** Entropiata Agency 
**Approved By:** [Business Manager]
