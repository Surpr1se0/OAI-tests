import re
import csv
import os


UE_NAME = "ue1"

log_file = os.path.join("pilot-analysis", "dirty-files", "pilot_" + UE_NAME + ".log")
output_csv = os.path.join("pilot-analysis", "clean-files", "dmrs_pdsch", "PDSCH_DMRS" + UE_NAME + ".csv")

header_re = re.compile(r"nr_pdsch_dmrs_rx dmrs config type (\d+) port (\d+) nb_pdsch_rb (\d+)")
wfwt_re = re.compile(r"wf\[(\d+)\] = (-?\d+)\s+wt\[(\d+)\]= (-?\d+)")
pilot_re = re.compile(r"i (\d+) pdsch mod_dmrs (-?\d+) (-?\d+)")

with open(log_file, "r") as f:
    content = f.read()

headers = header_re.findall(content)
wfwt = wfwt_re.findall(content)
pilots = pilot_re.findall(content)

if not (len(headers) == len(wfwt) == len(pilots)):
    print("warning: No of blocks do not match")
    print(f"Headers: {len(headers)}, wf/wt: {len(wfwt)}, pilots: {len(pilots)}")

with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ConfigType", "Port", "RBs", "wf_idx", "wf_val", "wt_idx", "wt_val", "i", "I Part", "Q Part"])

    for h, w, p in zip(headers, wfwt, pilots):
        writer.writerow([*h, *w, *p])

print(f"Data extracted to '{output_csv}' w/ {len(pilots)} entries.")
