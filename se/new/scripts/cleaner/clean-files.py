import re
import os

# General variables
scenarios = ["cf"]  # cell-free and cell-based
num_ues = ["5"]
base_dir_input = os.path.join("se", "new","dirty-files-ul")
base_dir_output = os.path.join("se", "new", "clean-files-ul")

# Novo regex com captura do SE
pattern = re.compile(
    r"\[\s*(\d+)\s*ms\]\s*\[UE\s+(\d+)\]\s*UL:\s*SNR\s*=\s*([+-]?\d+(?:\.\d+)?)\s*dB\s*\|\s*SE\s*=\s*([+-]?\d+(?:\.\d+)?)\s*bit/s/Hz\s*$",
    re.IGNORECASE
)

def extract_csv(input, output):
    with open(input, 'r') as f:
        lines = f.readlines()

    parsed_lines = []
    for line in lines:
        match = pattern.search(line)
        if match: 
          time_ms, ue_id, ul_snr_db, ul_se = match.groups()
          parsed_lines.append((time_ms, ue_id, ul_snr_db, ul_se))
    if not parsed_lines:
        print(f"No valid data found in {input}")
        return

    min_time = min(int(row[0]) for row in parsed_lines)

    with open(output, 'w') as f_out:
        f_out.write("Time_ms,UE_ID,UL_SNR_dB,UL_SE_bit_per_s_Hz\n")
        for time_ms, ue_id, ul_snr_db, ul_se in parsed_lines:
            norm_time = int(time_ms) - min_time
            f_out.write(f"{norm_time},{ue_id},{ul_snr_db},{ul_se}\n")

    print(f"Clean file created: {output}\n")

for scenario in scenarios:
    for num_ue in num_ues:
        for i in range(1, 30):
            filename = f"rep_{str(i).zfill(3)}"
            input_file = os.path.join(base_dir_input, scenario, num_ue, f"{filename}.log")
            output_file = os.path.join(base_dir_output, scenario, num_ue, f"{filename}.csv")
            extract_csv(input_file, output_file)

print("All files processed successfully.")
