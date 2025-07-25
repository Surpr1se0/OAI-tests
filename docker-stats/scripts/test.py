import re
import csv
import os
import pandas as pd

# Diretórios
raw_data_dir = os.path.join("docker-stats", "dirty-files")
output_dir = os.path.join("docker-stats", "clean-files")
os.makedirs(output_dir, exist_ok=True)

# Cabeçalho do CSV
header = [
    "Container_ID", "Name", "CPU_Usage_Percent", "Mem_Usage", "Mem_Limit",
    "Mem_Usage_Percent", "Net_RX", "Net_TX", "Block_Read", "Block_Write", "PIDs"
]

# Regex para cada linha de `docker stats`
pattern = re.compile(
    r'^(\S+)\s+'                 # Container ID
    r'(\S+)\s+'                  # Name
    r'([\d.]+%)\s+'              # CPU %
    r'([\d.]+[MGK]i?B)\s*/\s*'   # Mem Usage
    r'([\d.]+[MGK]i?B)\s+'       # Mem Limit
    r'([\d.]+%)\s+'              # Mem Usage %
    r'([\d.]+[TGMK]?B)\s*/\s*'   # Net RX
    r'([\d.]+[TGMK]?B)\s+'       # Net TX
    r'([\d.]+[TGMK]?B)\s*/\s*'   # Block Read
    r'([\d.]+[TGMK]?B)\s+'       # Block Write
    r'(\d+)$'                    # PIDs
)

# Conversão de unidades para MB
unit_factors = {
    'B': 1 / (1024 * 1024),
    'KB': 1 / 1024,
    'MB': 1,
    'GB': 1024,
    'TB': 1024 * 1024,
    'KiB': 1 / 1024,
    'MiB': 1,
    'GiB': 1024,
    'TiB': 1024 * 1024,
}

def convert_to_mb(value):
    try:
        number, unit = re.match(r"([\d.]+)([TGMK]?i?B)", value).groups()
        return round(float(number) * unit_factors[unit], 3)
    except:
        return None

# Processar todos os ficheiros .log
for filename in os.listdir(raw_data_dir):
    if not filename.endswith(".log"):
        continue

    input_path = os.path.join(raw_data_dir, filename)
    output_path = os.path.join(output_dir, filename.replace(".log", ".csv"))

    parsed_lines = []
    with open(input_path, 'r') as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                parsed_lines.append(list(match.groups()))

    # Gravar CSV original
    if parsed_lines:
        df = pd.DataFrame(parsed_lines, columns=header)

        # Adicionar conversões para MB
        df["Mem_Usage_MB"] = df["Mem_Usage"].apply(convert_to_mb)
        df["Mem_Limit_MB"] = df["Mem_Limit"].apply(convert_to_mb)
        df["Net_RX_MB"] = df["Net_RX"].apply(convert_to_mb)
        df["Net_TX_MB"] = df["Net_TX"].apply(convert_to_mb)
        df["Block_Read_MB"] = df["Block_Read"].apply(convert_to_mb)
        df["Block_Write_MB"] = df["Block_Write"].apply(convert_to_mb)

        # Guardar CSV convertido
        df.to_csv(output_path, index=False)
        print(f"✅ CSV gerado com sucesso: {output_path}")
    else:
        print(f"⚠️ Nenhuma linha válida encontrada em: {filename}")
