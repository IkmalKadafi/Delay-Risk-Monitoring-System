
# LaDe Last-Mile Analytics Platform

## Project Overview
This represents an enterprise-grade Decision Intelligence system for last-mile logistics. 
It uses the **LaDe dataset** (via HuggingFace) to predict SLA breaches using **XGBoost** and provides a **What-If Simulation Engine** to optimize operational thresholds based on financial risk.

## Key Features
- **Predictive Risk Modeling**: Real-time SLA breach probability using XGBoost.
- **Financial Risk Quantification**: Translates ML scores into monetary exposure (Rupiah).
- **What-If Simulation**: Interactive engine to test risk thresholds and cost parameters.
- **Executive & Ops Dashboards**: Tailored views for strategic and tactical decision-making.

## Architecture
- **Backend**: FastAPI (Python)
- **ML Core**: XGBoost, Scikit-Learn, Pandas
- **Frontend**: Vanilla JS, HTML5, Chart.js (Dark Mode Glassmorphism UI)
- **Data Source**: Cainiao-AI/LaDe (HuggingFace)

## Project Structure
```
lade_xgb_decision_web/
├── backend/
│   ├── app.py                 # API Server
│   ├── train_model.py         # Model Training Pipeline
│   ├── data_loader.py         # Data Ingestion (Streaming/Caching)
│   ├── decision_policy.py     # Threshold Logic
│   ├── what_if.py             # Simulation Engine
│   └── ...
├── frontend/
│   ├── index.html             # Landing Page
│   ├── simulation.html        # What-If Tool
│   ├── css/style.css          # UI Styles
│   └── js/                    # Client Logic
```

## How to Run

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Train the Model
This step downloads the dataset (or generates synthetic backup if offline), trains the XGBoost model, and saves artifacts.
```bash
cd backend
python train_model.py
```
*Note: The first run may take time to stream the dataset.*

### 3. Start the Server
```bash
cd backend
python app.py
```
The application will be available at **http://localhost:8000**.

## Usage Guide
1. **Landing**: Overview of the system flow.
2. **Dataset**: View sample records from LaDe.
3. **Ops Dashboard**: Monitor real-time risk distribution and required actions.
4. **Simulation**: Adjust the "Risk Threshold" slider. Observe how "Total Cost" changes. Find the sweet spot between "Intervention Cost" (FP) and "Missed SLA Penalty" (FN).
5. **Executive**: View high-level financial savings and compliance rates.
