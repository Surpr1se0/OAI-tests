import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import defaultdict
import os

# import data
ficheiro = os.path.join("throughput", "Cell-based-10ues.txt")  

# Read content of the file
with open(ficheiro, "r") as f:
    linhas = [linha.strip() for linha in f if linha.strip()]

# Regex to extract throughput values, through dictionary
dados_ues = defaultdict(list)

for linha in linhas:
    match = re.match(r"\[UE (\d+) \| RB \d+\] Throughput = ([\d\.]+)", linha)
    if match:
        ue = int(match.group(1))
        throughput = float(match.group(2))
        dados_ues[ue].append(throughput)

# Create DataFrames for each UE 
dfs = {}
for ue, valores in dados_ues.items():
    tempo = [i * 10 for i in range(len(valores))] 
    df = pd.DataFrame({
        "Time (ms)": tempo,
        "Throughput (Mbps)": valores
    })
    df["Rolling Avg (Mbps)"] = df["Throughput (Mbps)"].rolling(window=5).mean()
    dfs[ue] = df

# Graphic of Throughput and Rolling Average
plt.figure(figsize=(14, 6))
for ue, df in dfs.items():
    sns.lineplot(x="Time (ms)", y="Rolling Avg (Mbps)", data=df, label=f"UE {ue}")
plt.title("Rolling Avg (Mbps) for 5 UEs\n(Cell Based 10x UEs)")
plt.xlabel("Time (ms)")
plt.ylabel("Throughput (Mbps)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# main statistics
print("\nStatistics:\n")
print(df["Throughput (Mbps)"].describe())