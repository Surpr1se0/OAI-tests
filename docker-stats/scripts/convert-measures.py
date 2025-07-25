import pandas as pd
import os

unit_factors = {
    'B': 1 / (1024 * 1024),      # Bytes → MB
    'KB': 1 / 1024,              # KB → MB
    'MB': 1,
    'GB': 1024,
    'TB': 1024 * 1024,
    'KiB': 1 / 1024,
    'MiB': 1,
    'GiB': 1024,
    'TiB': 1024 * 1024
}

def convert_to_mb(value):
    try:
        number, unit = re.match(r"([\d.]+)([TGMK]?i?B)", value).groups()
        return float(number) * unit_factors[unit]
    except:
        return None

output_dir = os.path.join("docker-stats", "clean-files")
df = pd.read_csv(output_dir + "\\1.csv") ### CHANGE THIS TO YOUR INPUT CSV FILE

for col in ['Mem_Usage', 'Mem_Limit', 'Net_RX', 'Net_TX', 'Block_Read', 'Block_Write']:
    df[col + "_MB"] = df[col].apply(convert_to_mb)

df.drop(columns=['Mem_Usage', 'Mem_Limit', 'Net_RX', 'Net_TX', 'Block_Read', 'Block_Write'], inplace=True)

df.to_csv(output_dir + "\\docker_stats_converted.csv", index=False)
print("Conversão completa → 'docker_stats_converted.csv'")
