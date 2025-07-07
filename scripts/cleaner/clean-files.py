import re
import os

def extract_csv(input, output):
    pattern = re.compile(r"\[UE (\d+) \| RB (\d+)\] Throughput = ([\d.]+) Mbps")

    with open(input, 'r') as f:
        lines = f.readlines()

    with open(output, 'w') as f_out:
        f_out.write("UE_ID,RB_ID,Throughput_Mbps\n")  # header
        for linha in lines:
            match = pattern.search(linha)
            if match:
                ue_id, rb_id, throughput = match.groups()
                f_out.write(f"{ue_id},{rb_id},{throughput}\n")

    print(f"Clean file created: {output}\n")

base_dir = os.path.join("clean-files", "UL", "throughput", "4th-attempt", "cell-based", "10")

for i in range (1, 6): 
    input_file = os.path.join(base_dir, f"{i}.txt")
    output_file = os.path.join(base_dir, f"{i}.csv")
    extract_csv(input_file, output_file)