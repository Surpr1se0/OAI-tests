import re
import csv
import os


UE_NAME = "ue1"

log_file = os.path.join("pilot-analysis", "dirty-files", "pilot_" + UE_NAME + ".log")
output_csv = os.path.join("pilot-analysis", "clean-files", "PDCCH", "PDCHH_" + UE_NAME + ".csv")

pattern = re.compile(r"\[PDCCH-DMRS pilot\]\s*\[(\d+)\] = \((-?\d+), (-?\d+)\)")

with open(log_file, "r") as f:
    content = f.read()

matches = pattern.findall(content)

with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Index", "I Part", "Q Part"])
    for match in matches:
        writer.writerow(match)

print(f"Extracted {len(matches)} pilots PDCCH to '{output_csv}'")