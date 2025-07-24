import re
import os

base_dir_input = os.path.join("iperf", "dirty-files")
base_dir_output = os.path.join("iperf", "clean-files")

bandwidth = ["1", "5", "10", "50", "100", "200", "500"] 

pattern = re.compile(r"\[\s*(\d+)\]\s+(\d+\.\d+)-(\d+\.\d+)\s+sec\s+([\d.]+)\s+KBytes\s+([\d.]+)\s+Kbits/sec\s+([\d.]+)\s+ms\s+(\d+)/(\d+)\s+\(\d+%")

def extract_iperf_csv(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    parsed_lines = []
    for line in lines:
        match = pattern.search(line)
        if match:
            stream_id, t_start, t_end, kbytes, kbits_sec, latency_ms, lost, total = match.groups()
            parsed_lines.append((
                int(stream_id),
                float(t_start),
                float(t_end),
                float(kbytes),
                float(kbits_sec),
                float(latency_ms),
                int(lost),
                int(total)
            ))

    if not parsed_lines:
        print(f"No valid data found in {input_file}")
        return

    # Write in the csv file
    with open(output_file, 'w') as f_out:
        f_out.write("Stream_ID,Time_Start,Time_End,KBytes,Kbps,Latency_ms,Lost,Total\n")
        for row in parsed_lines:
            f_out.write(",".join(map(str, row)) + "\n")

    print(f"Clean File Created: {output_file}")

# process multiple files
for filename in os.listdir(base_dir_input):
    for bandwidth_value in bandwidth:
        for i in range (1,5):
            filename = f"rep_{str(i).zfill(3)}"
            input_file = os.path.join(base_dir_input, bandwidth_value, f"{filename}.log")
            output_file = os.path.join(base_dir_output, bandwidth_value, f"{filename}.csv")
            extract_iperf_csv(input_file, output_file)

print("Processing complete.")
