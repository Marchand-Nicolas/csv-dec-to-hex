"""
This python file takes a one column csv file, and converts each line (except the first) from int string to hex string.
collect csv files from the "in" folder, and save the converted csv files to the "out" folder, adding "_hex" to the file name.
"""

import csv
import sys
import os
import json

in_folder = "in"
out_folder = "out"


def convert_csv_to_hex(file_name):
    with open(file_name, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        lines = list(csv_reader)
        for i in range(1, len(lines)):
            lines[i] = [hex(int(lines[i][0]))]
    out_file_name = os.path.join(
        out_folder, os.path.basename(file_name).replace(".csv", "_hex.csv")
    )
    with open(out_file_name, "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(lines)


if len(sys.argv) != 1:
    print("Usage: python main.py")
    sys.exit(1)
if not os.path.exists(in_folder):
    print(f"Error: {in_folder} folder not found")
    sys.exit(1)
if not os.path.exists(out_folder):
    os.makedirs(out_folder)
for file_name in os.listdir(in_folder):
    if file_name.endswith(".csv"):
        convert_csv_to_hex(os.path.join(in_folder, file_name))


def convert_json_to_csv(file_name):
    # Ensure the output folder exists
    os.makedirs(out_folder, exist_ok=True)

    # Read the JSON file
    with open(file_name, "r") as json_file:
        data = json.load(json_file)

    # Check if the JSON is a valid format (keys as columns, values as rows)
    if not isinstance(data, dict):
        raise ValueError(
            "JSON content must be an object with keys as columns and values as rows."
        )

    # Extract columns (keys) and rows (values)
    columns = list(data.keys())
    rows = zip(*data.values())  # Transpose rows from the JSON data

    # Create output CSV file path
    csv_file_name = os.path.join(
        out_folder, os.path.splitext(os.path.basename(file_name))[0] + ".csv"
    )

    # Write to the CSV file
    with open(csv_file_name, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(columns)  # Write header
        writer.writerows(rows)  # Write rows


for file_name in os.listdir(in_folder):
    if file_name.endswith(".json"):
        convert_json_to_csv(os.path.join(in_folder, file_name))
print("Done")
