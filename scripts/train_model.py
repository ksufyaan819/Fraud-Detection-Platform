import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

def train_model():
    print("--- Starting Fraud Detection ML Pipeline ---")
    
    # 1. Setup Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Target the raw data generated in Part 1
    DATA_PATH = os.path.join(BASE_DIR, "ml", "data", "raw", "synthetic_transactions.csv")
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    MODEL_PATH = os.path.join(MODEL_DIR, "xgboost_model.json")

    # 2. Load Data
    print(f"Loading data from {DATA_PATH}...")
    try:
        # It is crucial to assign the loaded data explicitly to the variable 'df'
        # so it doesn't trigger a NameError later in the script.
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"❌ Error: Could not find data at {DATA_PATH}.")
        print("Please check that your Part 1 data generation step completed successfully.")
        return

    print("Splitting data into train and test sets...")
    
    # Detect the target column name (usually 'fraud' or 'is_fraud')
    target_col = 'is_fraud' if 'is_fraud' in df.columns else 'fraud'

    # 3. Preprocess Data
    # Drop columns that are not useful for prediction (like IDs and timestamps)
    X = df.drop(columns=[target_col, 'transaction_id', 'timestamp'], errors='ignore')
    y = df[target_col]

    # Fix XGBoost pandas_feature_info error: XGBoost cannot handle raw strings. 
    # We must convert the string 'merchant_category' to numeric values.
    if 'merchant_category' in X.columns:
        category_mapping = {"retail": 0, "travel": 1, "food": 2, "entertainment": 3}
        X['merchant_category'] = X['merchant_category'].str.lower().map(category_mapping).fillna(0)

    # 4. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Train XGBoost Model
    print("Starting model training...")
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'max_depth': 4,
        'learning_rate': 0.1
    }

    # Train the model
    model = xgb.train(
        params, 
        dtrain, 
        num_boost_round=100, 
        evals=[(dtest, 'test')], 
        early_stopping_rounds=10, 
        verbose_eval=False
    )

    # 6. Save Model to the /models/ folder
    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save_model(MODEL_PATH)
    print(f"✅ Pipeline Complete! Model successfully saved to: {MODEL_PATH}")

if __name__ == "__main__":
    train_model()