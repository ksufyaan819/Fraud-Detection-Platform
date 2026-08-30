import pandas as pd
import joblib
import sys
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.transaction import TransactionLog
from app.schemas.transaction import TransactionRequest, TransactionResponse, ExplainabilityResponse

# Point to the ml directory located at ML_PROJECT/fraud-detection-platform/ml
ML_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml"))
sys.path.append(ML_DIR)

try:
    from model_scorer import score_transaction
    from explainability import generate_explanation
except ImportError:
    print("Warning: ML scripts not found. Ensure Part 2 files are in the 'ml' folder.")

router = APIRouter()

MODEL_PATH = os.path.join(ML_DIR, "xgboost_fraud_model.pkl")
try:
    xgb_model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    xgb_model = None

FRAUD_THRESHOLD = 0.85 

@router.post("/score", response_model=TransactionResponse)
def score_endpoint(request: TransactionRequest, db: Session = Depends(get_db)):
    if xgb_model is None:
        raise HTTPException(status_code=500, detail="ML Model not loaded.")

    features_df = pd.DataFrame([request.dict(exclude={"transaction_id"})])
    risk_score = score_transaction(xgb_model, features_df)
    is_fraud = bool(risk_score >= FRAUD_THRESHOLD)

    db_log = TransactionLog(
        transaction_id=request.transaction_id,
        amount=request.amount,
        merchant_category=request.merchant_category,
        risk_score=risk_score,
        is_fraud=is_fraud
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return TransactionResponse(
        transaction_id=request.transaction_id,
        risk_score=risk_score,
        is_fraud=is_fraud,
        threshold_used=FRAUD_THRESHOLD
    )

@router.post("/explain", response_model=ExplainabilityResponse)
def explain_endpoint(request: TransactionRequest):
    if xgb_model is None:
        raise HTTPException(status_code=500, detail="ML Model not loaded.")

    features_df = pd.DataFrame([request.dict(exclude={"transaction_id"})])
    risk_score = score_transaction(xgb_model, features_df)
    explanation_data = generate_explanation(xgb_model, features_df)

    return ExplainabilityResponse(
        transaction_id=request.transaction_id,
        risk_score=risk_score,
        top_features=explanation_data.get("feature_importance", {}),
        base_value=explanation_data.get("base_value", 0.0)
    )