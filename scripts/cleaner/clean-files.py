import re
import os

scenarios = ["cf", "cb"] # cell-free and cell-based
reps = ["1", "5", "10"]  # can be 1, 5 or 10
base_dir_input = os.path.join("dirty-files")
base_dir_output = os.path.join("clean-files")

def extract_csv(input, output):
    pattern = re.compile(r"(\d+)\[UE (\d+) \| RB (\d+)\] Throughput = ([\d.]+) Mbps")

    with open(input, 'r') as f:
        lines = f.readlines()

    with open(output, 'w') as f_out:
        f_out.write("Time_ms,UE_ID,RB_ID,Throughput_Mbps\n")  # header
        for linha in lines:
            match = pattern.search(linha)
            if match:
                time_ms,ue_id, rb_id, throughput = match.groups()
                f_out.write(f"{time_ms},{ue_id},{rb_id},{throughput}\n")

    print(f"Clean file created: {output}\n")


for scenario in scenarios:
    for rep in reps:
        for i in range (1,30):
          filename = f"rep_{str(i).zfill(3)}" # make sure to have leading zeros

          input_file = os.path.join(base_dir_input, scenario,rep, f"{filename}.log")
          output_file = os.path.join(base_dir_output, scenario,rep, f"{filename}.csv")
          extract_csv(input_file, output_file)

print("All files processed successfully.")