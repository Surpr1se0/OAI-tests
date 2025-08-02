import os
import re
import csv

input_file = os.path.join("pilot-analysis", "dirty-files", "ue6_GS.txt")
output_file = os.path.join("pilot-analysis", "clean-files", "ue6_GS.csv")

PATTERNS = [
    re.compile(r"PBCH DMRS"),
    re.compile(r"PDCCH DMRS"),
    re.compile(r"UE DMRS"),
    re.compile(r"UE CSI DMRS")
]

def line_matches(line):
    return any(p.search(line) for p in PATTERNS)

def extract_fields(line):
    timestamp_match = re.match(r"(\d+\.\d+)", line)
    timestamp = timestamp_match.group(1) if timestamp_match else ""

    if "PBCH DMRS" in line: # nr_gold_pbch
        match = re.search(r"PBCH DMRS lmax (\d+), nid (\d+), symb (\d+), x2 (\w+)", line)
        if match:
            return [timestamp, "PBCH", match.group(1), match.group(2), "-", match.group(3), match.group(4)]
    elif "PDCCH DMRS" in line: # nr_gold_pdcch
        match = re.search(r"PDCCH DMRS slot (\d+), symb (\d+), Nid (\d+), x2 (\w+)", line)
        if match:
            return [timestamp, "PDCCH", "-", match.group(3), match.group(1), match.group(2), match.group(4)]
    elif "UE DMRS" in line: # nr_gold_pdsch OR nr_gold_pusch
        match = re.search(r"UE DMRS slot (\d+), symb (\d+), nscid (\d+), nid (\d+), x2 (\w+)", line)
        if match:
            return [timestamp, "PDSCH/PUSCH", "-", match.group(4), match.group(1), match.group(2), match.group(5)]
    elif "UE CSI DMRS" in line: # nr_gold_csi_rs
        match = re.search(r"UE CSI DMRS length \d+, x2 (\w+), nid (\w+)", line)
        if match:
            return [timestamp, "CSI", "-", match.group(2), "-", "-", match.group(1)]
    return None

def process_logs():
    with open(input_file, "r", encoding='utf-8') as infile, \
         open(output_file, "w", newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["TIMESTAMP", "TYPE", "Lmax", "Nid", "Slot", "Symbol", "x2"])

        for line in infile:
            if line_matches(line):
                fields = extract_fields(line)
                if fields:
                    writer.writerow(fields)

if __name__ == "__main__":
    process_logs()
