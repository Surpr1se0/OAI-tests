import re
import csv
import os

UE_NAME ="ue6"
LOG_FILE = os.path.join("rx-pilot-estimation", "dirty-files", UE_NAME + ".log")
CSV_FILE = os.path.join("rx-pilot-estimation", "clean-files", "PDCCH", UE_NAME + ".csv")

regex_patterns = {
    "pilot_indexed": re.compile(r"\[PDCCH-DMRS pilot\] \[(\d+)\] = \(([-\d]+), ([-\d]+)\)"),
    "pilot_info": re.compile(
        r"\[PDCCH\] pilot (?:\d+|%u) : rxF - > \(([-\d]+),([-\d]+)\) .*? ch -> \(([-\d]+),([-\d]+)\), pil -> \(([-\d]+),([-\d]+)\)"
    ),
    "pilot_compact": re.compile(
        r"\[PDCCH\] pilot\[(\d+)\] = \(([-\d]+), ([-\d]+)\)\s+rxF\[(\d+)\] = \(([-\d]+), ([-\d]+)\)"
    ),
}

parsed_rows = []

with open(LOG_FILE, "r") as f:
    for line in f:
        match = regex_patterns["pilot_info"].search(line)
        if match:
            rxF_r, rxF_i, ch_r, ch_i, pilot_r, pilot_i = map(int, match.groups())
            parsed_rows.append({
                "idx": len(parsed_rows),
                "rxF_r": rxF_r,
                "rxF_i": rxF_i,
                "ch_r": ch_r,
                "ch_i": ch_i,
                "pilot_r": pilot_r,
                "pilot_i": pilot_i,
                "k": None  # k não presente nesse print
            })
            continue

        match = regex_patterns["pilot_compact"].search(line)
        if match:
            idx, pilot_r, pilot_i, k, rxF_r, rxF_i = map(int, match.groups())
            parsed_rows.append({
                "idx": idx,
                "rxF_r": rxF_r,
                "rxF_i": rxF_i,
                "ch_r": None,
                "ch_i": None,
                "pilot_r": pilot_r,
                "pilot_i": pilot_i,
                "k": k
            })
            continue

        match = regex_patterns["pilot_indexed"].search(line)
        if match:
            idx, pilot_r, pilot_i = map(int, match.groups())
            parsed_rows.append({
                "idx": idx,
                "rxF_r": None,
                "rxF_i": None,
                "ch_r": None,
                "ch_i": None,
                "pilot_r": pilot_r,
                "pilot_i": pilot_i,
                "k": None
            })

with open(CSV_FILE, "w", newline="") as csvfile:
    fieldnames = ["idx", "rxF_r", "rxF_i", "ch_r", "ch_i", "pilot_r", "pilot_i", "k"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in parsed_rows:
        writer.writerow(row)

print(f"Ficheiro CSV gerado com sucesso: {CSV_FILE}")
