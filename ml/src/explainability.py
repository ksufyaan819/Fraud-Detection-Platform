import shap
import joblib
import pandas as pd
import numpy as np  # <-- Added missing import

class FraudExplainer:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)
        self.explainer = shap.TreeExplainer(self.model)

    def explain_instance(self, instance: pd.DataFrame) -> dict:
        shap_values = self.explainer.shap_values(instance)
        
        if len(shap_values.shape) > 1:
            shap_values = shap_values[0]
            
        feature_names = instance.columns.tolist()
        
        explanation = {
            feature: float(shap_value) 
            for feature, shap_value in zip(feature_names, shap_values)
        }
        
        sorted_explanation = dict(sorted(
            explanation.items(), 
            key=lambda item: abs(item[1]), 
            reverse=True
        ))
        
        return sorted_explanation

    def get_global_importance(self, X_background: pd.DataFrame) -> dict:
        shap_values = self.explainer.shap_values(X_background)
        
        # <-- Corrected: Must take the absolute value before calculating the mean
        mean_abs_shap = np.abs(shap_values).mean(axis=0) 
        
        feature_names = X_background.columns.tolist()
        importance_dict = {
            feature: float(importance) 
            for feature, importance in zip(feature_names, mean_abs_shap)
        }
        
        return dict(sorted(importance_dict.items(), key=lambda item: item[1], reverse=True))