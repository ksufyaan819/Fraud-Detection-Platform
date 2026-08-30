import joblib
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class FraudModelScorer:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        """Loads the serialized model from disk."""
        try:
            model = joblib.load(self.model_path)
            logger.info(f"Model loaded successfully from {self.model_path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model from {self.model_path}. Error: {e}")
            raise e

    def predict(self, features: pd.DataFrame) -> list:
        """Returns binary predictions (0 = Legitimate, 1 = Fraud)."""
        return self.model.predict(features).tolist()

    def predict_risk_score(self, features: pd.DataFrame) -> list:
        """Returns the probability (0.0 to 1.0) of a transaction being fraud."""
        # predict_proba returns an array of shape (n_samples, n_classes)
        # Index 1 is the probability of the positive class (fraud)
        probabilities = self.model.predict_proba(features)
        return probabilities[:, 1].tolist()