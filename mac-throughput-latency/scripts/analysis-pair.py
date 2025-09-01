import pandas as pd
import glob
import os
import numpy as np

RNTI_TO_LOGICAL_UE_2 = {
                 30040:  42234, 
}

RNTI_TO_LOGICAL_UE_1 = {
        30040:  42234,
        39999: 50104,
        19074: 11372,
        35620: 73211,
        41045: 12586,
}



RNTI_TO_LOGICAL_UE = {
                 30040: 42234, 
                 39999: 50104, 
                 19074: 11372, 
                 33930: 52644,
                 55955: 2379, 
                 7281: 53987,
                 5474: 5342, 
                 57717: 24556,
                 35620: 73211, 
                 41045: 12586
}

def analysis_per_mean(scenario, rep):
    base_input_dir = os.path.join("mac-throughput-latency", "clean-files-ul", scenario, rep)
    base_output_dir = os.path.join("mac-throughput-latency", "clean-files-ul", "aggr")

    # Read all csv files in the directory
    files = sorted(glob.glob(base_input_dir + "/*.csv"))
    reps = []

    for f in files:
        df = pd.read_csv(f)
        reps.append(df)
    df_total = pd.concat(reps)

    # Bin size de tempo (100 ms)
    bin_size = 100
    df_total['Time_ms'] = pd.to_numeric(df_total['Time_ms'], errors='coerce')
    df_total = df_total.replace([np.inf, -np.inf], np.nan)
    df_total = df_total.dropna(subset=['Time_ms'])
    df_total['Time_ms'] = (df_total['Time_ms'] / bin_size).round() * bin_size
    df_total['Time_ms'] = df_total['Time_ms'].astype(int)


    # map rnti
    df_total['logical_ue'] = df_total['UE_ID'].map(RNTI_TO_LOGICAL_UE)

    # remove entries without mapping
    df_total = df_total.dropna(subset=['logical_ue'])
    df_total['logical_ue'] = df_total['logical_ue'].astype(int)

    # group by time bin and logical ue and calculate mean and std throughput
    agg = df_total.groupby(['Time_ms', 'logical_ue']).agg(
        Mean_Throughput=('Throughput_Mbps', 'sum'),
        Std_Throughput=('Throughput_Mbps', 'std'),
    ).reset_index()
    agg = agg[['Time_ms', 'logical_ue', 'Mean_Throughput', 'Std_Throughput']]

    out_file = os.path.join(base_output_dir, f"agg-{scenario}-{rep}.csv")
    agg.to_csv(out_file, index=False)
    print(f"New file stored: {out_file}")


#analysis_per_mean("cf", "1")
#analysis_per_mean("cf", "5")
analysis_per_mean("cf", "10")