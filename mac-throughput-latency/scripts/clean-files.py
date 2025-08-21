import re
import os

# General variables
scenarios = ["cb"] # cell-free and cell-based
num_ues = ["1", "5", "10"]  # can be 1, 5 or 10
base_dir_input = os.path.join("mac-throughput-latency", "dirty-files-ul")
base_dir_output = os.path.join("mac-throughput-latency","clean-files-ul")

# Function to extract and clean the CSV data
def extract_csv(input, output):
    # regex adaptado
    pattern = re.compile(r"(\d+)\s+ms\s+\[UE\s+(\d+)\]\s+UL Throughput\s*=\s*([\d.]+)\s*Mbps")

    with open(input, 'r') as f:
        lines = f.readlines()

    parsed_lines = []
    for line in lines:
        match = pattern.search(line)
        if match:
            time_ms, ue_id, throughput = match.groups()
            parsed_lines.append((time_ms, ue_id, throughput))
    
    if not parsed_lines:
        print(f"No valid data found in {input}")
        return

    min_time = min(int(row[0]) for row in parsed_lines)

    with open(output, 'w') as f_out:
        f_out.write("Time_ms,UE_ID,RB_ID,Throughput_Mbps\n")
        for time_ms, ue_id, throughput in parsed_lines:
            norm_time = int(time_ms) - min_time
            f_out.write(f"{norm_time},{ue_id},-1,{throughput}\n")

    print(f"Clean file created: {output}\n")


for scenario in scenarios:
    for num_ue in num_ues:
        for i in range (1,30):
          filename = f"rep_{str(i).zfill(3)}" # make sure to have leading zeros

          input_file = os.path.join(base_dir_input, scenario,num_ue, f"{filename}.log")
          output_file = os.path.join(base_dir_output, scenario,num_ue, f"{filename}.csv")
          extract_csv(input_file, output_file)

print("All files processed successfully.")