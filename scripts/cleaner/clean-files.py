import re
import os

# General variables
scenarios = ["cf", "cb"] # cell-free and cell-based
num_ues = ["1", "5", "10"]  # can be 1, 5 or 10
base_dir_input = os.path.join("dirty-files")
base_dir_output = os.path.join("clean-files")

# Function to extract and clean the CSV data
def extract_csv(input, output):
    # regex
    pattern = re.compile(r"(\d+)\[UE (\d+) \| RB (\d+)\] Throughput = ([\d.]+) Mbps")

    # open the input file and read lines
    with open(input, 'r') as f:
        lines = f.readlines()

    # process each line
    parsed_lines = []
    for line in lines:
        match = pattern.search(line)
        if match:
            # extract the relevant data
            time_ms, ue_id, rb_id, throughput = match.groups()
            # convert to appropriate types
            parsed_lines.append((time_ms, ue_id, rb_id, throughput))
    
    # check if we have valid data
    if not parsed_lines:
        print(f"No valid data found in {input}")
        return

    # calculate the minimum time
    min_time = min(int(row[0]) for row in parsed_lines)

    # create the ouput file and write the header
    with open(output, 'w') as f_out:
        f_out.write("Time_ms,UE_ID,RB_ID,Throughput_Mbps\n")
        for time_ms, ue_id, rb_id, throughput in parsed_lines:
            norm_time = int(time_ms) - min_time # regularize the time to start from 0
            f_out.write(f"{norm_time},{ue_id},{rb_id},{throughput}\n")

    print(f"Clean file created: {output}\n")


for scenario in scenarios:
    for num_ue in num_ues:
        for i in range (1,30):
          filename = f"rep_{str(i).zfill(3)}" # make sure to have leading zeros

          input_file = os.path.join(base_dir_input, scenario,num_ue, f"{filename}.log")
          output_file = os.path.join(base_dir_output, scenario,num_ue, f"{filename}.csv")
          extract_csv(input_file, output_file)

print("All files processed successfully.")