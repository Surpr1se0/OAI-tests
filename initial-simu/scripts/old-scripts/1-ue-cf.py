import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# import data
file = os.path.join("throughput", "Cell-free-1ue.txt")

# Read content of the file
with open(file, 'r') as f:
    raw_data = f.read()

# Regex to extract throughput values
throughput_values = [float(val) for val in re.findall(r"Throughput\s*=\s*([\d\.]+)", raw_data)]

# Create a DataFrame
df = pd.DataFrame({
    "Time (ms)": [i * 10 for i in range(len(throughput_values))],
    "Throughput (Mbps)": throughput_values
})

# Calculate rolling average with a window of 5
df["Rolling Avg (Mbps)"] = df["Throughput (Mbps)"].rolling(window=5).mean()

# Grafic of Throughput and Rolling Average 
plt.figure(figsize=(14, 6))
sns.lineplot(x="Time (ms)", y="Throughput (Mbps)", data=df, label="Throughput")
sns.lineplot(x="Time (ms)", y="Rolling Avg (Mbps)", data=df, label="Rolling Avg (5)")
plt.title("Throughput in time\n(Cell Free 1x UE)")
plt.xlabel("Time (ms)")
plt.ylabel("Throughput (Mbps)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# main statistics
print("\nStatistics:\n")
print(df["Throughput (Mbps)"].describe())