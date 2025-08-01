import pandas as pd

# Fetch from GitHub (direct raw link)
csv_url = "https://github.com/angel-one/smartapi-python/raw/main/instrument_files/NSE.csv"
df = pd.read_csv(csv_url)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Check columns
print("Available Columns:", df.columns.tolist())

# Lookup symboltoken for INFY-EQ
row = df[df["symbol"] == "INFY-EQ"]
if row.empty:
    print("Symbol not found.")
else:
    print(row[["symboltoken", "symbol", "name"]])
