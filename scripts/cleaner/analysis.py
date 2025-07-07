import pandas as pd
import glob
import os

base_dir = os.path.join("clean-files", "UL", "throughput", "4th-attempt", "cell-based", "10")
output_dir = os.path.join("clean-files", "UL", "throughput", "4th-attempt", "cell-based", "10")

# Read all csv files in the directory
files = sorted(glob.glob(base_dir + "/*.csv"))
reps = []

for idx, f in enumerate(files):
    df = pd.read_csv(f)

    # Cria um índice de tempo com base na posição da linha
    df['Time'] = df.groupby('UE_ID').cumcount()
    df['Rep'] = idx + 1
    reps.append(df)

# Concatenate all dataframes into one
df_total = pd.concat(reps)

# Calculate avg and std deviation per UE and Time
agg = df_total.groupby(['Time', 'UE_ID']).agg(
    Mean_Throughput=('Throughput_Mbps', 'mean'),
    Std_Throughput=('Throughput_Mbps', 'std')
).reset_index()

# Export csv consolidated data
agg.to_csv(base_dir + "/cb-10-aggregated.csv", index=False)
print(f"File stored in {base_dir}\n")

# Read the aggregated CSV file
df = pd.read_csv(base_dir + "/cb-10-aggregated.csv")

# Substitute time with real time in milliseconds
df['Real_time_ms'] = df['Time'] * 10
df = df.drop(columns=['Time'])
df = df.rename(columns={'Real_time_ms': 'Time_ms'})

# Reorganize the columns
df = df[['Time_ms', 'UE_ID', 'Mean_Throughput', 'Std_Throughput']]

# store new csv
df.to_csv(base_dir + "/cb-10-aggregated.csv", index=False)
print(f"New updated file stored in {base_dir}\n")
