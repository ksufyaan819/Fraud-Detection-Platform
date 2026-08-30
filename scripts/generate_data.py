# /fraud-detection-platform/scripts/generate_data.py

import os
import sys
from pathlib import Path

# Add the root directory to the Python path so we can import from ml.src
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from ml.src.data_generator import DataGenerator

def main():
    # Ensure the data directories exist
    raw_data_dir = root_dir / "ml" / "data" / "raw"
    os.makedirs(raw_data_dir, exist_ok=True)
    
    output_file = raw_data_dir / "synthetic_transactions.csv"
    
    print("Generating synthetic transactions...")
    generator = DataGenerator(random_state=42)
    # Generating 15,000 rows for a solid train/test split
    df = generator.generate_transactions(n_samples=15000, start_date='2024-01-01')
    
    generator.save_data(df, str(output_file))
    print("Data generation complete.")

if __name__ == "__main__":
    main()