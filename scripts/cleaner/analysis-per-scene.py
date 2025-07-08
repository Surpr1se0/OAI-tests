import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from matplotlib.ticker import MultipleLocator
import re

base_dir = os.path.join("clean-files", "UL", "throughput", "4th-attempt", "cell-based", "10")
output_dir = os.path.join("clean-files", "UL", "throughput", "4th-attempt", "cell-based", "10")

base_path = os.path.join("clean-files", "UL", "throughput", "4th-attempt")
cenarios = ["cell-based", "cell-free"]
num_ues = 10

df_total = pd.DataFrame()

# Loop over scenarios and UEs
for scenario in cenarios:
    folder_path = os.path.join(base_path, scenario, str(num_ues))

    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(folder_path, filename)
        rep = filename.replace(".txt", "")

        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        dados_ues = defaultdict(list)
        for line in lines:
            match = re.match(r"\[UE (\d+) \| RB \d+\] Throughput = ([\d\.]+)", line)
            if match:
                ue = int(match.group(1))
                throughput = float(match.group(2))
                dados_ues[ue].append(throughput)

        for ue, values in dados_ues.items():
            time = [i * 10 for i in range(len(values))]
            df = pd.DataFrame({
                "Time (ms)": time,
                "Throughput (Mbps)": values,
                "UE": ue,
                "Scenario": "cb" if scenario == "cell-based" else "cf",
                "Num_UEs": num_ues,
                "Repetition": rep
            })
            df_total = pd.concat([df_total, df], ignore_index=True)

# Save 
df_total = df_total.sort_values(by=["Scenario", "Repetition", "Time (ms)"]).reset_index(drop=True)
df_total.to_csv(base_dir + "/cb-10-per-scene.csv", index=False)
print(f"File stored in {base_dir}\n")
