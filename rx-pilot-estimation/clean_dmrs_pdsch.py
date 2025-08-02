import re
import csv
import os
import pandas as pd


UE_NAME = "ue1"

log_file = os.path.join("rx-pilot-estimation", "dirty-files", UE_NAME + ".log")
output_csv = os.path.join("rx-pilot-estimation", "clean-files", "PDSCH", UE_NAME + ".csv")

data = []

with open(log_file, "r") as f:
    lines = f.readlines()

for line in lines:
    # Pilot
    match = re.search(r"\[PDSCH-DMRS pilot\] \[(\d+)\] = \(([-\d]+), ([-\d]+)\)", line)
    if match:
        i, r, im = map(int, match.groups())
        data.append({"type": "pilot", "index": i, "I": r, "Q": im})
        continue

    # rxF
    match = re.search(r"\[PDSCH-RX\] aarx=(\d+) i=(\d+) rxF = \(([-\d]+),([-\d]+)\)", line)
    if match:
        aarx, i, r, im = map(int, match.groups())
        data.append({"type": "rxF", "antenna": aarx, "index": i, "I": r, "Q": im})
        continue

    # dl_ch
    match = re.search(r"\[PDSCH-RX\](\d+)\s+(\d+)", line)
    if match:
        r, im = map(int, match.groups())
        data.append({"type": "dl_ch", "I": r, "Q": im})

df = pd.DataFrame(data)
df.to_csv(output_csv, index=False)




