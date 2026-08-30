import xgboost as xgb
import joblib
from sklearn.metrics import classification_report, roc_auc_score, average_precision_score
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudModelTrainer:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = xgb.XGBClassifier(
            objective='binary:logistic',
            eval_metric='aucpr', # Area under PR curve is better for imbalanced fraud data
            use_label_encoder=False,
            random_state=self.random_state,
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            scale_pos_weight=10 # Assuming fraud is rare; adjust based on Part 1 data
        )

    def train(self, X_train: pd.DataFrame, y_train: pd.Series, X_val: pd.DataFrame = None, y_val: pd.Series = None):
        """Trains the XGBoost model on the provided dataset."""
        logger.info("Starting model training...")
        
        eval_set = [(X_train, y_train)]
        if X_val is not None and y_val is not None:
            eval_set.append((X_val, y_val))
            
        self.model.fit(
            X_train, 
            y_train,
            eval_set=eval_set,
            verbose=10
        )
        logger.info("Model training completed.")
        return self.model

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series):
        """Evaluates the model using Precision-Recall, ROC-AUC, and F1."""
        logger.info("Evaluating model performance...")
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]

        auc_roc = roc_auc_score(y_test, y_proba)
        auc_pr = average_precision_score(y_test, y_proba)
        
        print("\n--- Model Evaluation ---")
        print(f"ROC-AUC Score: {auc_roc:.4f}")
        print(f"PR-AUC Score:  {auc_pr:.4f}\n")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        
        return {"roc_auc": auc_roc, "pr_auc": auc_pr}

    def save_model(self, filepath: str):
        """Saves the trained model to disk."""
        joblib.dump(self.model, filepath)
        logger.info(f"Model successfully saved to {filepath}")