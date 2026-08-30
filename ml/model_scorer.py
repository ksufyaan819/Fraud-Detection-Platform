import pandas as pd

def score_transaction(model, features_df: pd.DataFrame) -> float:
    """Scores a transaction using the loaded XGBoost model."""
    
    # 1. Convert text categories to numeric codes (just like we did in training)
    for col in features_df.select_dtypes(include=['object', 'string']).columns:
        features_df[col] = features_df[col].astype('category').cat.codes
        
    # 2. Get the probability that the transaction is fraud (class 1)
    probabilities = model.predict_proba(features_df)
    risk_score = float(probabilities[0][1])
    
    return risk_score