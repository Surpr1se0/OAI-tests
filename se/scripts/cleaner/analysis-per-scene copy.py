import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from matplotlib.ticker import MultipleLocator
import re

cenarios = ["cb", "cf"]
num_ues = ["1", "5", "10"]

base_input_dir = os.path.join("clean-files-ul")
base_output_dir = os.path.join("clean-files-ul", "aggr")

df_total = pd.DataFrame()

# Loop over scenarios and UEs
for scenario in cenarios:
    for num_ue in num_ues:
        folder = os.path.join(base_input_dir, str(scenario), str(num_ues))
        files = sorted(glob.glob(os.path.join(folder, "rep_*.csv")))

        for idx, filepath in enumerate(files):
            df = pd.read_csv(filepath)
            df['Repetition'] = idx + 1 # Add repetition number
            df['Scenario'] = scenario
            df['Num_UEs'] = int(num_ue)
            df_total = pd.concat([df_total, df], ignore_index=True)

# Reorganize the columns
df_total = df_total.sort_values(by=["Scenario", "Num_UEs", "Time_ms"]).reset_index(drop=True)

# Save
df_total.to_csv(base_output_dir + "/total-per-scene.csv", index=False)
print(f"File stored in {base_output_dir}\n")
