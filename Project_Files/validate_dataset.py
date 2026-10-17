
import csv
import os
from collections import Counter

path = r"D:\Mens_T20_Project\Processed_Dataset\mens_t20_processed.csv"

if not os.path.isfile(path):
    raise SystemExit("ERROR: Processed CSV not found.")

match_rows = Counter()
match_dates = Counter()
row_count = 0
empty_match_ids = 0
bad_width_rows = 0

with open(path, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    headers = reader.fieldnames or []

    required = [
        "match_id", "start_date", "season", "venue",
        "batting_team", "bowling_team", "gender",
        "team_type", "match_type"
    ]

    missing_columns = [c for c in required if c not in headers]

    if missing_columns:
        print("WARNING: Missing expected columns:", missing_columns)

    for row in reader:
        row_count += 1
        match_id = (row.get("match_id") or "").strip()

        if not match_id:
            empty_match_ids += 1
            continue

        match_rows[match_id] += 1

        date = (row.get("start_date") or "").strip()
        if date:
            match_dates[match_id] += 1

print("\n========== VALIDATION REPORT ==========")
print("Rows:", row_count)
print("Columns:", len(headers))
print("Unique match IDs:", len(match_rows))
print("Rows without match ID:", empty_match_ids)
print("File size (MB):", round(os.path.getsize(path) / (1024 * 1024), 2))
print("Smallest match record count:", min(match_rows.values(), default=0))
print("Largest match record count:", max(match_rows.values(), default=0))
print("Matches with a date:", len(match_dates))
print("Required columns missing:", missing_columns)

print("\nValidation completed.")
