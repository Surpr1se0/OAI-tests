import pandas as pd
import glob
import os

def analysis_latency(scenario, rep):
    base_input_dir = os.path.join("mac-throughput-latency", "clean-files-latency", scenario, rep)
    base_output_dir = os.path.join("mac-throughput-latency", "clean-files-latency", "aggr")

    # Lê todos os ficheiros *_latency.csv
    files = sorted(glob.glob(base_input_dir + "/*.csv"))
    reps = []

    for idx, f in enumerate(files):
        df = pd.read_csv(f)
        reps.append(df)
    
    df_total = pd.concat(reps)

    bin_size = 100  # ms
    df_total['Time_ms'] = (df_total['Time_ms'] / bin_size).round() * bin_size
    df_total['Time_ms'] = df_total['Time_ms'].astype(int)

    # Calcular média e desvio padrão por time bin
    agg = df_total.groupby(['Time_ms']).agg(
        Mean_Latency_us=('Latency_us', 'mean'),
        Std_Latency_us=('Latency_us', 'std')
    ).reset_index()

    # Reorganizar colunas
    agg = agg[['Time_ms', 'Mean_Latency_us', 'Std_Latency_us']]

    # Guardar
    os.makedirs(base_output_dir, exist_ok=True)
    out_path = os.path.join(base_output_dir, f"agg-{scenario}-{rep}.csv")
    agg.to_csv(out_path, index=False)
    print(f"New latency file stored in {base_output_dir} for {scenario}-{rep}\n")



analysis_latency("cb", "1")
analysis_latency("cb", "5")
analysis_latency("cb", "10")

#analysis_latency("cf", "1")
#analysis_latency("cf", "5")
#analysis_latency("cf", "10")  