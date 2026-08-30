# /fraud-detection-platform/ml/src/feature_engineering.py

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.scaler = StandardScaler()
        self.category_columns = ['merchant_category']
        self.numerical_columns = ['amount', 'user_age_days']
        
        # We will learn the exact columns during fit() to handle one-hot encoding consistency
        self.feature_columns_ = None 

    def fit(self, X: pd.DataFrame, y=None):
        X_transformed = self._transform_internal(X, fit_scaler=True)
        self.feature_columns_ = X_transformed.columns.tolist()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_transformed = self._transform_internal(X, fit_scaler=False)
        
        # Ensure all columns from training are present (handle unseen categorical variables)
        for col in self.feature_columns_:
            if col not in X_transformed.columns:
                X_transformed[col] = 0
                
        # Return only the columns used in training, in the exact same order
        return X_transformed[self.feature_columns_]

    def _transform_internal(self, X: pd.DataFrame, fit_scaler: bool = False) -> pd.DataFrame:
        df = X.copy()
        
        # 1. Temporal features
        if 'timestamp' in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            df['hour_of_day'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
            df = df.drop(columns=['timestamp'])

        # 2. Drop identifiers
        cols_to_drop = [col for col in ['transaction_id', 'user_id', 'is_fraud'] if col in df.columns]
        df = df.drop(columns=cols_to_drop)

        # 3. Categorical encoding (One-Hot)
        if 'merchant_category' in df.columns:
            df = pd.get_dummies(df, columns=self.category_columns, drop_first=True, dtype=float)

        # 4. Numerical scaling
        existing_num_cols = [c for c in self.numerical_columns if c in df.columns]
        if existing_num_cols:
            if fit_scaler:
                df[existing_num_cols] = self.scaler.fit_transform(df[existing_num_cols])
            else:
                df[existing_num_cols] = self.scaler.transform(df[existing_num_cols])
                
        return df