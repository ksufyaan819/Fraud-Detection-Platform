# Fraud Detection Command Center

An end-to-end Machine Learning pipeline and live monitoring platform built to detect, score, and explain fraudulent financial transactions in real-time.

Unlike standard "black-box" models, this platform prioritizes **Explainable AI (XAI)** by utilizing SHAP (SHapley Additive exPlanations) to provide human-readable insights into exactly **why** a transaction was flagged.

## 🚀 Tech Stack

* **Frontend:** React, Vite, JavaScript, CSS
* **Backend:** FastAPI, Python, Pydantic
* **Machine Learning:** XGBoost (Classification), SHAP (Explainability), Pandas, NumPy

## 🧠 Key Features

* **Real-Time Transaction Scoring:** REST API endpoint that accepts transaction payloads and returns a live fraud probability score using a trained XGBoost model.
* **Explainable AI (XAI) Investigation Queue:** A dedicated dashboard for analysts to review flagged transactions, featuring dynamic SHAP value charts that break down the exact feature contributions (e.g., amount, distance from home) driving the model's decision.
* **Live Monitoring Dashboard:** High-level metrics tracking total transactions scanned, fraud caught, and overall model accuracy.

## 💻 Local Setup & Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/ksufyaan819/Fraud-Detection-Platform.git](https://github.com/ksufyaan819/Fraud-Detection-Platform.git)
cd fraud-detection-platform