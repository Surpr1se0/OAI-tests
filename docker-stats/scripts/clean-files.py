import re
import csv
import os

raw_data_dir = os.path.join("docker-stats", "dirty-files")
output_dir = os.path.join("docker-stats", "clean-files")

header = [
    "Container_ID", "Name",
    "CPU_Usage_Percent",
    "Mem_Usage", "Mem_Limit", "Mem_Usage_Percent",
    "Net_RX", "Net_TX",
    "Block_Read", "Block_Write",
    "PIDs"
]

pattern = re.compile(
    r'^(\S+)\s+'                # Container ID
    r'(\S+)\s+'                 # Name
    r'([\d.]+%)\s+'             # CPU %
    r'([\d.]+[MG]iB)\s*/\s*'    # Mem Usage
    r'([\d.]+[MG]iB)\s+'        # Mem Limit
    r'([\d.]+%)\s+'             # Mem Usage %
    r'([\d.]+[TGMK]?B)\s*/\s*'  # Net RX
    r'([\d.]+[TGMK]?B)\s+'      # Net TX
    r'([\d.]+[TGMK]?B)\s*/\s*'  # Block Read
    r'([\d.]+[TGMK]?B)\s+'      # Block Write
    r'(\d+)$'                   # PIDs
)

def read_raw_data(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    parsed_lines = []
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            parsed_lines.append(list(match.groups()))
    return parsed_lines

for filename in os.listdir(raw_data_dir):
    if filename.endswith(".log"):
        input_path = os.path.join(raw_data_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".log", ".csv"))

        rows = read_raw_data(input_path)

        if rows:
            with open(output_path, "w", newline="") as f_out:
                writer = csv.writer(f_out)
                writer.writerow(header)
                writer.writerows(rows)
            print(f"Converted file {output_path}")
        else:
            print(f"No converted file {input_path}")




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

df = pd.read_csv("docker_stats.csv")

# Aplicar conversão para colunas relevantes
for col in ['Mem_Usage', 'Mem_Limit', 'Net_RX', 'Net_TX', 'Block_Read', 'Block_Write']:
    df[col + "_MB"] = df[col].apply(convert_to_mb)

# Remover colunas antigas (opcional)
df.drop(columns=['Mem_Usage', 'Mem_Limit', 'Net_RX', 'Net_TX', 'Block_Read', 'Block_Write'], inplace=True)

# Guardar novo CSV
df.to_csv("docker_stats_converted.csv", index=False)
print("Conversão completa → 'docker_stats_converted.csv'")