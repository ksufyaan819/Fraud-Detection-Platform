from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime

# UNCOMMENTED: Importing your actual ML module
from ml.explainer import FraudExplainer  

app = FastAPI(title="Fraud Detection API")

# Initialize your ML explainer (Loads the XGBoost model and SHAP globally on startup)
fraud_model = FraudExplainer()

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# MOCK DATA STORE (To be replaced by Postgres in Part 8!)
# ==========================================
RECENT_TRANSACTIONS = {
    "tx_1001": {"amount": 4500, "distance_from_home": 120, "is_high_risk_merchant": 1},
    "tx_1002": {"amount": 12, "distance_from_home": 2, "is_high_risk_merchant": 0},
    "tx_1003": {"amount": 850, "distance_from_home": 45, "is_high_risk_merchant": 1},
    # Add this one!
    "tx_1004": {"amount": 8900, "distance_from_home": 185, "is_high_risk_merchant": 1}, 
}

# ==========================================
# PART 1-5 ENDPOINTS (Live Dashboard & Manual Scoring)
# ==========================================

@app.post("/api/score")
async def score_transaction(payload: Dict[str, Any]):
    """Endpoint for the Manual Transaction Testing form."""
    
    # 1. Safely map React's keys (likely camelCase) to XGBoost's expected snake_case keys
    # If a key is missing, it defaults to 0 to prevent crashes
    formatted_payload = {
        "amount": float(payload.get("amount", 0.0)),
        "distance_from_home": float(payload.get("distance_from_home", payload.get("distanceFromHome", 0.0))),
        "is_high_risk_merchant": int(payload.get("is_high_risk_merchant", payload.get("isHighRiskMerchant", 0)))
    }
    
    # 2. Pass the safely formatted payload to the real XGBoost model
    score = fraud_model.predict(formatted_payload)
    
    # 3. Determine prediction threshold (e.g., > 0.70 is fraud)
    is_fraud = score > 0.70
    
    return {
        "status": "success",
        "score": round(score, 2), 
        "prediction": "fraud" if is_fraud else "safe",
        "message": "Transaction scored by XGBoost successfully."
    }

@app.get("/api/stats")
async def get_stats():
    return {
        "totalScanned": 1250,
        "fraudCaught": 42,
        "xgboostAccuracy": 94.5,
        "accuracy": 94.5 
    }

@app.get("/api/transactions/recent")
async def get_recent_transactions():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return [
        {
            "id": "tx_998", "amount": 25.00, "prediction": "safe", 
            "score": 0.05, "riskScore": 5, "timestamp": now, "status": "Clean"
        },
        {
            "id": "tx_999", "amount": 1450.50, "prediction": "fraud", 
            "score": 0.92, "riskScore": 92, "timestamp": now, "status": "Fraud"
        },
    ]

# ==========================================
# PART 6 & 7 ENDPOINTS (Investigation & Real SHAP Explainability)
# ==========================================

class ExplanationResponse(BaseModel):
    transaction_id: str
    fraud_score: float
    factors: List[dict]

@app.get("/api/v1/investigate")
async def get_flagged_transactions():
    """Returns historical transactions flagged for review."""
    # Score them on the fly for the dashboard (or read from a DB in the future)
    flagged = []
    for tx_id, tx_data in RECENT_TRANSACTIONS.items():
        score = fraud_model.predict(tx_data)
        if score > 0.70:
            flagged.append({"id": tx_id, "score": round(score, 2), **tx_data})
    return flagged

@app.get("/api/v1/explain/{transaction_id}", response_model=ExplanationResponse)
async def explain_score(transaction_id: str):
    """Returns the REAL SHAP explanation for why a transaction got its score."""
    if transaction_id not in RECENT_TRANSACTIONS:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    tx_data = RECENT_TRANSACTIONS[transaction_id]
    
    # Get real score
    score = fraud_model.predict(tx_data)
    
    # Get real SHAP factors formatted as [{"feature": "amount", "contribution": 1.45}, ...]
    real_factors = fraud_model.explain(tx_data)
    
    return ExplanationResponse(
        transaction_id=transaction_id,
        fraud_score=round(score, 2),
        factors=real_factors
    )