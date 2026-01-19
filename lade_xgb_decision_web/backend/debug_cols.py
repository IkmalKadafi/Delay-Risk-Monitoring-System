
from data_loader import load_lade_data
import sys

try:
    df = load_lade_data(sample_size=10)
    print("Columns found:", df.columns.tolist())
    with open('cols_debug.txt', 'w') as f:
        f.write(str(df.columns.tolist()))
except Exception as e:
    print(f"Error: {e}")
