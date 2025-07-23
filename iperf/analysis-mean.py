import pandas as pd
import glob
import os

def analysis_per_mean(scenario):
  base_input_dir = os.path.join("iperf", "clean-files", scenario)
  base_output_dir = os.path.join("iperf", "clean-files", scenario)

  # Read all csv files in the directory
  files = sorted(glob.glob(base_input_dir + "/*.csv"))
  dfs = []

  # Concatenate all dataframes into one
  for f in files:
        df = pd.read_csv(f)
        dfs.append(df)

  df_total = pd.concat(dfs)

  # Usar Time_Start como referência de tempo (em segundos)
  df_total['Time_s'] = df_total['Time_Start'].astype(float).round().astype(int)

  # Agregação por Time_s e Stream_ID
  agg = df_total.groupby(['Time_s', 'Stream_ID']).agg(
        Mean_Kbps=('Kbps', 'mean'),
        Std_Kbps=('Kbps', 'std'),
        Mean_Latency_ms=('Latency_ms', 'mean'),
        Std_Latency_ms=('Latency_ms', 'std')
    ).reset_index()

  # Organizar colunas
  agg = agg[['Time_s', 'Stream_ID', 'Mean_Kbps', 'Std_Kbps', 'Mean_Latency_ms', 'Std_Latency_ms']]

  # Guardar CSV
  output_file = os.path.join(base_output_dir, f"agg-{scenario}.csv")
  agg.to_csv(output_file, index=False)

  print(f"Ficheiro de agregação criado: {output_file}")

# Exemplo de uso
analysis_per_mean("1")
analysis_per_mean("5")