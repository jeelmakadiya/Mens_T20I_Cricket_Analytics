
import csv
import os
import math
from collections import Counter

TARGET_ROWS = 150_000

input_path = input(
    "Enter the full path of your original CSV: "
).strip().strip('"')

output_path = input(
    "Enter the full path for the processed CSV: "
).strip().strip('"')

if not os.path.isfile(input_path):
    raise SystemExit("ERROR: Original CSV file not found.")

if os.path.abspath(input_path) == os.path.abspath(output_path):
    raise SystemExit("ERROR: Output must not overwrite the original.")

os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)


def open_csv(path):
    return open(
        path, "r", encoding="utf-8-sig",
        errors="replace", newline=""
    )


print("\nPass 1: Counting rows for each match...")

match_info = {}
total_rows = 0

with open_csv(input_path) as file:
    sample = file.read(65536)
    file.seek(0)

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel

    reader = csv.DictReader(file, dialect=dialect)
    headers = reader.fieldnames

    if not headers or "match_id" not in headers:
        raise SystemExit("ERROR: match_id column was not found.")

    for row in reader:
        total_rows += 1
        match_id = (row.get("match_id") or "").strip()

        if not match_id:
            continue

        if match_id not in match_info:
            match_info[match_id] = {
                "rows": 0,
                "date": (row.get("start_date") or "").strip()
            }

        match_info[match_id]["rows"] += 1

if not match_info:
    raise SystemExit("ERROR: No valid match IDs found.")

matches = sorted(
    match_info.items(),
    key=lambda item: (
        item[1]["date"] or "9999",
        item[0]
    )
)

average_rows = total_rows / len(matches)
target_matches = min(
    len(matches),
    max(1, round(TARGET_ROWS / average_rows))
)

print("Original rows:", total_rows)
print("Unique matches:", len(matches))
print("Average rows per match:", round(average_rows, 1))
print("Target number of complete matches:", target_matches)

# Select matches spread across the chronological match list.
# The final row count will be approximate because matches
# have different numbers of deliveries.
selected_ids = set()

for i in range(target_matches):
    index = min(
        len(matches) - 1,
        math.floor((i + 0.5) * len(matches) / target_matches)
    )
    selected_ids.add(matches[index][0])

expected_rows = sum(
    match_info[mid]["rows"] for mid in selected_ids
)

print("Expected selected rows:", expected_rows)
print("\nPass 2: Writing selected complete matches...")

written_rows = 0
blank_counts = Counter()

with open_csv(input_path) as source, open(
    output_path, "w", encoding="utf-8-sig", newline=""
) as destination:

    reader = csv.DictReader(source, dialect=dialect)
    writer = csv.DictWriter(
        destination,
        fieldnames=headers,
        dialect=dialect,
        extrasaction="ignore"
    )
    writer.writeheader()

    for row in reader:
        match_id = (row.get("match_id") or "").strip()

        if match_id not in selected_ids:
            continue

        cleaned = {}

        for column in headers:
            value = row.get(column)

            if value is None:
                value = ""

            value = value.strip()

            if value == "":
                blank_counts[column] += 1

            cleaned[column] = value

        writer.writerow(cleaned)
        written_rows += 1

output_size_mb = os.path.getsize(output_path) / (1024 * 1024)

print("\n========== PROCESSING REPORT ==========")
print("Original rows:", total_rows)
print("Selected complete matches:", len(selected_ids))
print("Processed rows:", written_rows)
print("Processed columns:", len(headers))
print("Output file size:", round(output_size_mb, 2), "MB")
print("Output file:", output_path)

if written_rows > TARGET_ROWS:
    print(
        "NOTE: The output exceeds 150,000 rows because "
        "complete matches were preserved."
    )

if output_size_mb > 70:
    print(
        "NOTE: The file exceeds 70 MB. We can optimize "
        "columns and storage after verifying requirements."
    )

print("\nWhitespace was trimmed and blank cells normalized.")
print("No columns were removed.")
print("The original CSV was not modified.")
print("Processing complete.")
