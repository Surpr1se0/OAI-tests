import re
import csv
import os


UE_NAME = "ue6"

log_file = os.path.join("rx-pilot-estimation", "dirty-files", UE_NAME + ".log")
output_csv = os.path.join("rx-pilot-estimation", "clean-files", "pbch", UE_NAME + ".csv")

pattern_pilot = re.compile(r'\[PBCH\] pilot (\d+): rxF= \(([-\d]+),([-\d]+)\), ch= \(([-\d]+),([-\d]+)\), pil=\(([-\d]+),([-\d]+)\)')
pattern_k = re.compile(r'\[PBCH\] k (\d+), first_carrier (\d+)')

entries = []
first_carrier = None

with open(log_file, "r") as f:
    for line in f:
        match_k = pattern_k.search(line)
        if match_k:
            k = int(match_k.group(1))
            first_carrier = int(match_k.group(2))

        match = pattern_pilot.search(line)
        if match:
            idx = int(match.group(1))
            rxF_r = int(match.group(2))
            rxF_i = int(match.group(3))
            ch_r = int(match.group(4))
            ch_i = int(match.group(5))
            pil_r = int(match.group(6))
            pil_i = int(match.group(7))

            entries.append({
                "idx": idx,
                "rxF_r": rxF_r,
                "rxF_i": rxF_i,
                "ch_r": ch_r,
                "ch_i": ch_i,
                "pilot_r": pil_r,
                "pilot_i": pil_i,
                "k": k if 'k' in locals() else '',
                "first_carrier": first_carrier if first_carrier is not None else ''
            })

with open(output_csv, "w", newline="") as csvfile:
    fieldnames = ["idx", "rxF_r", "rxF_i", "ch_r", "ch_i", "pilot_r", "pilot_i", "k", "first_carrier"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(entries)

print(f"Ficheiro CSV gerado: {output_csv}")
