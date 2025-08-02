import re
import csv
import os

input_file = os.path.join("pilot-analysis", "dirty-files","oai_dmrs_log.txt")

output_file = os.path.join("pilot-analysis", "clean-files","oai_dmrs_log.csv")

regex = re.compile(r"(PUSCH|PDSCH) DMRS MASK in HEX:([0-9A-Fa-f]+)")

data = []

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        match = regex.search(line)
        if match:
            dmrs_type = match.group(1)
            hex_mask = match.group(2)
            bin_mask = bin(int(hex_mask, 16))[2:].zfill(12)  # 12 bit binary
            pos = bin_mask.count("1")
            data.append({
                "type": dmrs_type,
                "hex_mask": hex_mask,
                "bin_mask": bin_mask,
                "pos": pos
            })

with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ["type", "hex_mask", "bin_mask", "pos"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for entry in data:
        writer.writerow(entry)

print(f"File generated: {output_file}")
