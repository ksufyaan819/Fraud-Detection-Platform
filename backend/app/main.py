from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import random

# Initialize the FastAPI app
app = FastAPI(title="Fraud Detection ML Pipeline")

# Configure CORS so the Vite frontend (port 5173) can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data structure for incoming transactions
# (You can add your specific XGBoost feature names here later)
class TransactionData(BaseModel):
    amount: float
    # Example additional features:
    # merchant_type: int
    # time_of_day: int
    
    class Config:
        # This prevents the app from crashing if the frontend sends extra fields
        extra = "allow" 

# ==========================================
# PART 1: MANUAL TRANSACTION SCORING
# ==========================================

@app.post("/api/v1/score")
async def score_transaction(transaction: TransactionData):
    """
    Receives data from the Manual Testing form on the frontend.
    TODO: Replace the mock logic below with your actual XGBoost predict() code.
    """
    # Example of how you will integrate your model later:
    # input_data = pd.DataFrame([transaction.dict()])
    # prediction = xgboost_model.predict(input_data)
    
    # Mock ML response to keep the frontend error-free during Part 5
    mock_probability = random.uniform(0.01, 0.99)
    is_fraud = mock_probability > 0.85
    
    return {
        "riskScore": round(mock_probability * 100, 1),
        "isFraud": is_fraud,
        "message": "Scored successfully (Simulated Data)"
    }

# ==========================================
# PART 5: LIVE DASHBOARD MONITORING
# ==========================================

@app.get("/api/stats")
async def get_fraud_stats():
    """
    Returns high-level metrics for the dashboard's StatCards.
    TODO: Replace with actual database/model metrics in Part 6.
    """
    return {
        "totalScanned": 24508,
        "fraudCaught": 142,
        "modelAccuracy": "94.8%"
    }

@app.get("/api/transactions/recent")
async def get_recent_transactions():
    """
    Returns a list of recent transactions for the FraudAlertsTable.
    Generates dynamic dummy data so the frontend table updates live every 10 seconds.
    """
    transactions = []
    
    # Generate 5 dynamic recent transactions
    for i in range(5):
        # Weight the randomness so most transactions show as clean
        is_fraud = random.random() > 0.85 
        
        transactions.append({
            "id": f"{random.randint(100000, 999999)}",
            "timestamp": (datetime.now() - timedelta(seconds=i*15)).isoformat(),
            "amount": round(random.uniform(15.50, 2500.00), 2),
            "riskScore": round(random.uniform(85.0, 99.9) if is_fraud else random.uniform(1.0, 40.0), 1),
            "isFraud": is_fraud
        })
        
    return transactions