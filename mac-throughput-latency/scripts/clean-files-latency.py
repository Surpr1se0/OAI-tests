import re
import os

# General variables
scenarios = ["cb"] # cell-free and cell-based
num_ues = ["1", "5", "10"]  # can be 1, 5 or 10
base_dir_input = os.path.join("mac-throughput-latency", "dirty-files-ul")
base_dir_output = os.path.join("mac-throughput-latency","clean-files-latency")

# Function to extract and clean the CSV data
def extract_latency_csv(input, output):
    pattern = re.compile(r"(\d+)\s+ms\s+\|\s+now=(\d+)\s+us\s+\|\s+PDCP ind_msg latency=(\d+)\s+us")

    with open(input, 'r') as f:
        lines = f.readlines()

    parsed = []
    for line in lines:
        m = pattern.search(line)
        if m:
            time_ms, now_ts, latency_us = m.groups()
            parsed.append((int(time_ms), int(now_ts), int(latency_us)))

    if not parsed:
        return

    min_time = min(row[0] for row in parsed)
    with open(output, "w") as f_out:
        f_out.write("Time_ms,Now_us,Latency_us\n")
        for time_ms, now_ts, latency_us in parsed:
            norm_time = time_ms - min_time
            f_out.write(f"{norm_time},{now_ts},{latency_us}\n")


for scenario in scenarios:
    for num_ue in num_ues:
        for i in range (1,30):
          filename = f"rep_{str(i).zfill(3)}" # make sure to have leading zeros

          input_file = os.path.join(base_dir_input, scenario,num_ue, f"{filename}.log")
          output_file = os.path.join(base_dir_output, scenario,num_ue, f"{filename}.csv")
          extract_latency_csv(input_file, output_file)

print("All files processed successfully.")