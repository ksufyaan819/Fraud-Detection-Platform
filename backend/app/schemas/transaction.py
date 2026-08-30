from pydantic import BaseModel, Field
from typing import Dict

class TransactionRequest(BaseModel):
    transaction_id: str
    amount: float = Field(..., gt=0)
    merchant_category: str
    distance_from_home: float
    distance_from_last_transaction: float
    ratio_to_median_purchase_price: float
    used_chip: int
    used_pin_number: int
    online_order: int

class TransactionResponse(BaseModel):
    transaction_id: str
    risk_score: float
    is_fraud: bool
    threshold_used: float

class ExplainabilityResponse(BaseModel):
    transaction_id: str
    risk_score: float
    top_features: Dict[str, float]
    base_value: float