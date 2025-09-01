import pandas as pd
import glob
import os
import numpy as np

def aggregate_cf(df, ue_map, overhead=1.0):
    results = []
    for ue_name, ue_ids in ue_map.items():
        df_sub = df[df["UE_ID"].isin(ue_ids)]
        for t, group in df_sub.groupby("Time_ms"):
            # Convert into SNR linear scale
            snr_linear = 10**(group["UL_SNR_dB"].to_numpy()/10.0)
            snr_total = snr_linear.sum()
            se_total = overhead * np.log2(1 + snr_total)
            results.append({
                "Time_ms": t,
                "UE_ID": ue_name,
                "Mean_SNR_dB": snr_total,
                "Mean_UL_SE_bit_per_s_Hz": se_total
            })
    return pd.DataFrame(results)

def analysis_per_mean(scenario, rep, ue_map=None, overhead=1.0):
    base_input_dir = os.path.join("se", "new", "clean-files-ul", scenario, rep)
    base_output_dir = os.path.join("se", "new", "clean-files-ul", "aggr")

    files = sorted(glob.glob(base_input_dir + "/*.csv"))
    reps = [pd.read_csv(f) for f in files]
    df_total = pd.concat(reps)

    bin_size = 100  # ms
    df_total['Time_ms'] = (df_total['Time_ms'] / bin_size).round() * bin_size
    df_total['Time_ms'] = df_total['Time_ms'].astype(int)

    df_agg = aggregate_cf(df_total, ue_map, overhead)

    outname = f"agg-{scenario}-{rep}-agg.csv"
    df_agg.to_csv(os.path.join(base_output_dir, outname), index=False)
    print(f"New file stored in {base_output_dir} for {scenario}-{rep}\n")

ue_map_example = {
    0: [1171, 5256],
    1: [8279, 920],
    2: [12524, 14002],
    3: [14350, 14608],
    4: [18432, 37624],
    5: [40142, 46443],
    6: [47098, 54141],
    7: [54487, 55143],
    8: [55839, 55499],
    9: [60232, 55862]
}

ue_map_example_1 = {
    0: [1382, 2609],
    1: [5794, 16233],
    2: [64248, 65104],
    3: [17950, 32893],
    4: [33135, 38070],
}


ue_map_example_2 ={
    0: [16233, 32893]
}

#analysis_per_mean("cf", "1", ue_map=ue_map_example_2, overhead=0.95)
analysis_per_mean("cf", "5", ue_map=ue_map_example_1, overhead=0.95)
#analysis_per_mean("cf", "10", ue_map=ue_map_example, overhead=0.95)
