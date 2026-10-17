
import csv
import os
from collections import Counter

file_path = input("Enter the full path of your original CSV: ").strip().strip('"')

if not os.path.isfile(file_path):
    print("ERROR: File not found.")
    input("Press Enter to exit...")
    raise SystemExit

print("\nReading dataset for audit. Please wait...")

try:
    with open(file_path, "r", encoding="utf-8-sig", errors="replace", newline="") as f:
        sample = f.read(65536)
        f.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel

        reader = csv.DictReader(f, dialect=dialect)

        rows = 0
        missing = Counter()
        match_ids = set()
        seasons = Counter()
        genders = Counter()
        team_types = Counter()
        match_types = Counter()
        teams = set()
        venues = set()
        duplicate_rows = 0
        seen_rows = set()

        for row in reader:
            rows += 1

            normalized = tuple(
                (row.get(col) or "").strip()
                for col in reader.fieldnames
            )

            if normalized in seen_rows:
                duplicate_rows += 1
            else:
                seen_rows.add(normalized)

            for col in reader.fieldnames:
                if not (row.get(col) or "").strip():
                    missing[col] += 1

            match_id = (row.get("match_id") or "").strip()
            if match_id:
                match_ids.add(match_id)

            for col, counter in [
                ("season", seasons),
                ("gender", genders),
                ("team_type", team_types),
                ("match_type", match_types)
            ]:
                value = (row.get(col) or "").strip()
                counter[value if value else "[BLANK]"] += 1

            for col in ["batting_team", "bowling_team"]:
                value = (row.get(col) or "").strip()
                if value:
                    teams.add(value)

            venue = (row.get("venue") or "").strip()
            if venue:
                venues.add(venue)

    print("\n========== DATA QUALITY AUDIT ==========")
    print("Total rows:", rows)
    print("Total unique match IDs:", len(match_ids))
    print("Total exact duplicate rows:", duplicate_rows)
    print("Total distinct teams:", len(teams))
    print("Total distinct venues:", len(venues))

    print("\nMissing values by column:")
    for col, count in sorted(missing.items()):
        if count:
            print(f"{col}: {count} ({count / rows * 100:.2f}%)")

    print("\nGender values and row counts:", genders.most_common())
    print("\nTeam type values and row counts:", team_types.most_common())
    print("\nMatch type values and row counts:", match_types.most_common())
    print("\nSeason values and row counts:")
    for value, count in seasons.most_common():
        print(f"{value}: {count}")

    print("\nTeam names:")
    print(sorted(teams))

    print("\nAudit complete. No source data was changed.")

except Exception as e:
    print("Audit failed:", e)

input("\nPress Enter to close...")
