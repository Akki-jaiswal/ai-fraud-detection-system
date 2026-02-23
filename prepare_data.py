import pandas as pd
from pathlib import Path

# Set up paths
data_dir = Path("data")
input_file = data_dir / "spam.csv"
output_file = data_dir / "training_data.csv"

def format_dataset():
    print(f"Loading raw dataset from {input_file}...")
    
    # Read the Kaggle CSV (it often has encoding issues, so we use latin-1)
    df = pd.read_csv(input_file, encoding='latin-1')
    
    # The dataset has extra unnamed columns we don't need, so we keep only v1 and v2
    df = df[['v1', 'v2']]
    
    # Rename the columns to match what your Fraud Detector expects
    df = df.rename(columns={'v1': 'label', 'v2': 'text'})
    
    # Convert 'spam' to 1 (Fraud) and 'ham' to 0 (Normal)
    df['label'] = df['label'].map({'spam': 1, 'ham': 0})
    
    # Save it as the file your main script looks for!
    df.to_csv(output_file, index=False)
    
    print(f"Success! Formatted {len(df)} rows.")
    print(f"Fraud cases: {df['label'].sum()}")
    print(f"Normal cases: {len(df) - df['label'].sum()}")
    print(f"Saved ready-to-use dataset to {output_file}")

if __name__ == "__main__":
    format_dataset()