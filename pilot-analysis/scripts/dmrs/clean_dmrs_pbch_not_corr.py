import re
import csv
import os


UE_NAME = "ue1"

log_file = os.path.join("pilot-analysis", "dirty-files", "pilot_" + UE_NAME + ".log")
output_csv = os.path.join("pilot-analysis", "clean-files", "dmrs_pbch_not_corr", "PBCH_DMRS_not_corr" + UE_NAME + ".csv")

gold_re = re.compile(r"nr_gold_pbch\[\(m<<1\)>>5\] ([a-fA-F0-9]+)")
output_re = re.compile(r"m (\d+)\s+output (-?\d+)\s+(-?\d+)")

with open(log_file, "r") as f:
    content = f.read()

gold = gold_re.findall(content)
output = output_re.findall(content)

with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["m", "gold_word_hex", "output_r", "output_i"])
    
    for gold, (m, r, i) in zip(gold, output):
        writer.writerow([m, gold, r, i])

print(f"Data extracted to '{output_csv}' w/ {len(gold)} entries.")
