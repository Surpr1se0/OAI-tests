import re
import csv
import os


UE_NAME = "ue1"

log_file = os.path.join("pilot-analysis", "dirty-files", "pilot_" + UE_NAME + ".log")
output_csv = os.path.join("pilot-analysis", "clean-files", "dmrs_pdcch", "PDCHH_DMRS" + UE_NAME + ".csv")

pattern = re.compile(r"i (\d+)\s+pdcch mod_dmrs\s+(-?\d+)\s+(-?\d+)")

# Leitura do ficheiro de log
with open(log_file, "r") as f:
    content = f.read()

# Encontrar todos os matches
matches = pattern.findall(content)

# Escrever para CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["i", "output_r", "output_i"])
    for match in matches:
        writer.writerow(match)


print(f"Extracted {len(matches)} pilots PDCCH to '{output_csv}'")