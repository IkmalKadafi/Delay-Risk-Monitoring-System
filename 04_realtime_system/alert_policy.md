# Alert Policy & Escalation Rules

**Version:** 2.0 (Real-Time Enabled)  
**Effective Date:** Jan 2026

---

## 1. Overview
This policy governs the automated actions triggered by the **SLA Risk Monitoring System**. It defines "Who does What" when a risk is detected.

## 2. Risk Bands

| Level | Probability Range | Severity | Definition |
| :--- | :--- | :--- | :--- |
| **High** | 70% - 100% | Critical | Delivery is fundamentally jeopardized. Without action, it WILL be late. |
| **Medium** | 40% - 69% | Warning | Delivery is struggling. Has a chance to recover if monitored. |
| **Low** | 0% - 39% | Normal | Standard delivery flow. |

## 3. Trigger Conditions & Actions

### A. High Risk (Critical)
*   **Trigger:** `probability >= 0.70` AND `time_elapsed < 80%`
*   **System Action:**
    1.  Push notification to **Area Manager** app: "Critical Delay Risk: Task [ID]".
    2.  Flag order in **Dispatch Dashboard** with RED border.
*   **Ops Procedure:**
    1.  Call Courier immediately.
    2.  If Courier is stuck/unresponsive -> **Action: Re-Assign** to nearest standby driver.
    3.  If traffic is logged -> **Action: Notify Customer** of revised ETA (Customer Service).

### B. Medium Risk (Warning)
*   **Trigger:** `probability >= 0.40`
*   **System Action:**
    1.  Add to "Watchlist" tab in Dashboard.
    2.  Send automated in-app message to Courier: "Are you facing issues with Order [ID]?"
*   **Ops Procedure:**
    1.  No manual call required yet.
    2.  Monitor for 15 mins. If status doesn't change -> Escalate to High.

## 4. Feedback Loop
*   Every manual intervention (Call, Re-assign) must be logged in the system with a "Reason Code".
*   This data will be used to retrain the model (e.g., if we re-assign and it saves the order, that's a positive label for the intervention).

## 5. Override Authority
*   **Dispatchers** have full authority to override the system decision if they have local context (e.g., "I know this driver is fast, ignore risk").
*   All overrides are logged for audit.
