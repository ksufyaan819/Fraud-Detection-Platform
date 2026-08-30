import xgboost as xgb
import shap
import pandas as pd

class FraudExplainer:
    def __init__(self):
        # 1. Load the XGBoost model
        self.model = xgb.XGBClassifier()
        self.model.load_model("ml/fraud_model.json")
        
        # 2. Initialize the SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)
        
        # 3. Define the exact features your model expects
        self.features = ["amount", "distance_from_home", "is_high_risk_merchant"]

    def _prepare_data(self, payload: dict) -> pd.DataFrame:
        """Converts FastAPI JSON payload into a Pandas DataFrame."""
        df = pd.DataFrame([payload])
        # Ensure columns are in the exact order the model expects
        return df[self.features]

    def predict(self, payload: dict) -> float:
        """Returns the probability of fraud (0.0 to 1.0)"""
        df = self._prepare_data(payload)
        # predict_proba returns [[prob_safe, prob_fraud]]
        return float(self.model.predict_proba(df)[0][1])

    def explain(self, payload: dict) -> list:
        """Returns SHAP values to explain the prediction."""
        df = self._prepare_data(payload)
        shap_values = self.explainer.shap_values(df)
        
        # Pair each feature with its SHAP contribution score
        factors = []
        for feature, contribution in zip(self.features, shap_values[0]):
            factors.append({
                "feature": feature,
                "contribution": float(contribution)
            })
            
        # Sort factors from most impactful to least impactful
        factors.sort(key=lambda x: abs(x["contribution"]), reverse=True)
        return factors