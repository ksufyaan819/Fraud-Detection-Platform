from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from app.db.database import Base

class TransactionLog(Base):
    __tablename__ = "transaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    amount = Column(Float)
    merchant_category = Column(String)
    risk_score = Column(Float)
    is_fraud = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)