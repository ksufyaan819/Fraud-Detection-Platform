import pandas as pd

def generate_explanation(model, features_df: pd.DataFrame) -> dict:
    """
    Generates a feature importance explanation for the transaction.
    In a full production environment, this would use the SHAP library.
    """
    # Returning a structured dictionary that matches our FastAPI schema
    return {
        "feature_importance": {
            "amount": 0.45,
            "distance_from_home": 0.35,
            "merchant_category": 0.20
        },
        "base_value": 0.1
    }