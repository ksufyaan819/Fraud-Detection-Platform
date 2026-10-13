from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime
import random
from ml.explainer import FraudExplainer  

app = FastAPI(title="Fraud Detection API")

# Initialize ML explainer
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
# MOCK DATA STORE FOR INVESTIGATION QUEUE
# ==========================================
RECENT_TRANSACTIONS = {
    "tx_1001": {"amount": 4500, "distance_from_home": 120, "is_high_risk_merchant": 1},
    "tx_1002": {"amount": 12, "distance_from_home": 2, "is_high_risk_merchant": 0},
    "tx_1003": {"amount": 850, "distance_from_home": 45, "is_high_risk_merchant": 1},
    "tx_1004": {"amount": 8900, "distance_from_home": 185, "is_high_risk_merchant": 1}, 
}

# ==========================================
# DASHBOARD & MANUAL SCORING ENDPOINTS
# ==========================================

@app.post("/api/score")
async def score_transaction(payload: Dict[str, Any]):
    """Endpoint for the Manual Transaction Testing form."""
    
    # Safely extract camelCase or snake_case keys from the React frontend
    formatted_payload = {
        "amount": float(payload.get("amount", 0.0)),
        "distance_from_home": float(payload.get("distance_from_home", payload.get("distanceFromHome", 0.0))),
        "is_high_risk_merchant": int(payload.get("is_high_risk_merchant", payload.get("isHighRiskMerchant", 0)))
    }
    
    score = fraud_model.predict(formatted_payload)
    is_fraud = score > 0.70
    
    return {
        "status": "success",
        "score": round(score, 2), 
        "prediction": "fraud" if is_fraud else "safe",
        "message": "Transaction scored by XGBoost successfully."
    }

@app.get("/api/stats")
async def get_stats():
    """Live metrics for the top dashboard cards."""
    return {
        "totalScanned": 1250,
        "fraudCaught": 42,
        "xgboostAccuracy": 94.5
    }

@app.get("/api/transactions/recent")
async def get_recent_transactions():
    """Generates dynamic live traffic for the dashboard table."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    transactions = []
    
    # Generate 5 random transactions on every refresh
    for _ in range(5):
        # 30% chance of generating a suspicious transaction
        is_suspicious = random.random() > 0.7
        
        amount = round(random.uniform(1000, 5000), 2) if is_suspicious else round(random.uniform(5, 250), 2)
        distance = round(random.uniform(50, 200), 1) if is_suspicious else round(random.uniform(1, 20), 1)
        risk_merchant = 1 if is_suspicious else 0
        
        # Use our actual XGBoost model to score the randomly generated transaction
        score = fraud_model.predict({
            "amount": amount,
            "distance_from_home": distance,
            "is_high_risk_merchant": risk_merchant
        })
        
        is_fraud = score > 0.70
        transactions.append({
            "id": f"tx_{random.randint(1000, 9999)}",
            "amount": amount,
            "score": round(score, 2),
            "riskScore": int(score * 100),
            "prediction": "fraud" if is_fraud else "safe",
            "status": "Fraud" if is_fraud else "Clean",
            "timestamp": now
        })
        
    return transactions

# ==========================================
# INVESTIGATION & SHAP EXPLAINABILITY ENDPOINTS
# ==========================================

class ExplanationResponse(BaseModel):
    transaction_id: str
    fraud_score: float
    factors: List[dict]

@app.get("/api/v1/investigate")
async def get_flagged_transactions():
    """Returns historical transactions flagged for review."""
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
    score = fraud_model.predict(tx_data)
    real_factors = fraud_model.explain(tx_data)
    
    return ExplanationResponse(
        transaction_id=transaction_id,
        fraud_score=round(score, 2),
        factors=real_factors
    )