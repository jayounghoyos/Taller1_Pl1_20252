import pandas as pd
import json

# Load CSV
csv_path = "movies_initial.csv"   # adjust if needed
df = pd.read_csv(csv_path)

# Convert DataFrame to list of dicts
records = df.to_dict(orient="records")

# Write JSON without escaping slashes
json_path = "movies.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"JSON file saved to {json_path}")
