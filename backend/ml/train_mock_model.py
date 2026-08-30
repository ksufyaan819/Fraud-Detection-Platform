import xgboost as xgb
import pandas as pd
import numpy as np
import os

# 1. Generate 100 rows of synthetic data
np.random.seed(42)

# 50 Safe Transactions (Low amount, close to home, low risk)
safe_amount = np.random.uniform(5, 50, 50)
safe_distance = np.random.uniform(1, 10, 50)
safe_risk = np.zeros(50)

# 50 Fraud Transactions (High amount, far from home, high risk)
fraud_amount = np.random.uniform(1000, 5000, 50)
fraud_distance = np.random.uniform(50, 200, 50)
fraud_risk = np.ones(50)

X = pd.DataFrame({
    "amount": np.concatenate([safe_amount, fraud_amount]),
    "distance_from_home": np.concatenate([safe_distance, fraud_distance]),
    "is_high_risk_merchant": np.concatenate([safe_risk, fraud_risk])
})
y = np.concatenate([np.zeros(50), np.ones(50)]) # 0 = Safe, 1 = Fraud

# 2. Train the XGBoost Classifier
print("Training mock model on 100 rows...")
model = xgb.XGBClassifier(eval_metric='logloss')
model.fit(X, y)

# 3. Save the model
save_path = os.path.join(os.path.dirname(__file__), "fraud_model.json")
model.save_model(save_path)

print(f"Success! Mock model saved to: {save_path}")