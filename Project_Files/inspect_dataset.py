
import csv
import os

file_path = input("Enter the full path of your CSV file: ").strip().strip('"')

if not os.path.isfile(file_path):
    print("ERROR: File not found. Check the path and try again.")
    input("Press Enter to exit...")
    raise SystemExit

print("\nFile size:", round(os.path.getsize(file_path) / (1024 * 1024), 2), "MB")
print("Inspecting CSV... Please wait.\n")

try:
    with open(file_path, "r", encoding="utf-8-sig", errors="replace", newline="") as file:
        sample = file.read(65536)
        file.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel

        reader = csv.reader(file, dialect)

        headers = next(reader, None)
        if not headers:
            print("ERROR: The CSV appears to be empty.")
            raise SystemExit

        headers = [h.strip() for h in headers]
        print("COLUMNS:")
        for number, header in enumerate(headers, start=1):
            print(f"{number}. {header}")

            print("\nALL COLUMN NAMES:")
            print(headers) 

        print("\nFIRST 5 DATA ROWS:")
        row_count = 0
        for row in reader:
            row_count += 1
            if row_count <= 5:
                print(row[:min(len(row), 12)])

        print("\nTotal data rows:", row_count)
        print("Total columns:", len(headers))
        print("Inspection completed.")

except (OSError, csv.Error) as error:
    print("Could not inspect the file:", error)

input("\nPress Enter to close...")
