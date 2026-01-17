
import pandas as pd
df = pd.read_parquet('data_cache/lade_data.parquet')
with open('cols.txt', 'w') as f:
    f.write('\n'.join(df.columns.tolist()))
    f.write('\n\nSample:\n')
    f.write(str(df.head(1).iloc[0]))
