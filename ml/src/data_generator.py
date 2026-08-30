# /fraud-detection-platform/ml/src/data_generator.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataGenerator:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        np.random.seed(self.random_state)
        self.categories = ['retail', 'travel', 'food', 'entertainment', 'digital_goods']

    def generate_transactions(self, n_samples: int = 10000, start_date: str = '2023-01-01') -> pd.DataFrame:
        """Generates synthetic transaction data with injected fraud patterns."""
        start_ts = datetime.strptime(start_date, '%Y-%m-%d')
        
        # Generate base features
        data = {
            'transaction_id': [f'txn_{i:07d}' for i in range(n_samples)],
            'user_id': np.random.randint(1000, 5000, n_samples),
            'timestamp': [start_ts + timedelta(minutes=int(np.random.gamma(2, 20) * i)) for i in range(n_samples)],
            'amount': np.random.lognormal(mean=3, sigma=1, size=n_samples).round(2),
            'merchant_category': np.random.choice(self.categories, n_samples, p=[0.4, 0.15, 0.3, 0.1, 0.05]),
            'user_age_days': np.random.randint(1, 1000, n_samples),
            'is_international': np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        }
        
        df = pd.DataFrame(data)
        
        # Inject realistic fraud patterns
        df['is_fraud'] = 0
        
        # Pattern 1: High amounts have higher fraud probability
        high_amount_mask = df['amount'] > 500
        df.loc[high_amount_mask, 'is_fraud'] = np.random.choice([0, 1], size=high_amount_mask.sum(), p=[0.7, 0.3])
        
        # Pattern 2: International travel/digital goods transactions
        risk_category_mask = df['merchant_category'].isin(['travel', 'digital_goods']) & (df['is_international'] == 1)
        df.loc[risk_category_mask, 'is_fraud'] = np.random.choice([0, 1], size=risk_category_mask.sum(), p=[0.4, 0.6])
        
        # Pattern 3: Late night transactions (02:00 - 05:00)
        hour = df['timestamp'].dt.hour
        night_mask = (hour >= 2) & (hour <= 5)
        df.loc[night_mask, 'is_fraud'] = np.random.choice([0, 1], size=night_mask.sum(), p=[0.6, 0.4])
        
        return df

    def save_data(self, df: pd.DataFrame, filepath: str):
        """Saves the generated DataFrame to a CSV file."""
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}. Total records: {len(df)}, Fraud rate: {df['is_fraud'].mean():.2%}")