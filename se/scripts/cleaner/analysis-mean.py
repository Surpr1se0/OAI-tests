import pandas as pd
import glob
import os

def analysis_per_mean(scenario, rep):
  base_input_dir = os.path.join("se", "clean-files-ul", scenario, rep)
  base_output_dir = os.path.join("se", "clean-files-ul", "aggr")

  # Read all csv files in the directory
  files = sorted(glob.glob(base_input_dir + "/*.csv"))
  reps = []

  # Concatenate all dataframes into one
  for idx, f in enumerate(files):
      df = pd.read_csv(f)
      reps.append(df)
  df_total = pd.concat(reps)

  bin_size = 100 # ms
  df_total['Time_ms'] = (df_total['Time_ms'] / bin_size).round() * bin_size
  df_total['Time_ms'] = df_total['Time_ms'].astype(int) # Convert to int

  # Calculate avg and std deviation per UE and Time
  agg_tp = df_total.groupby(['Time_ms', 'UE_ID']).agg(
      Mean_Throughput=('Throughput_Mbps', 'mean'),
      Std_Throughput=('Throughput_Mbps', 'std')
  ).reset_index()

  agg_se = df_total.groupby(['Time_ms', 'UE_ID']).agg(
      Mean_SE=('SE_bit_per_s_Hz', 'mean'),
      Std_SE=('SE_bit_per_s_Hz', 'std')
  ).reset_index()

  # Merge and Reorganize the columns
  agg = pd.merge(agg_tp, agg_se, on=['Time_ms', 'UE_ID'])
  agg = agg[['Time_ms', 'UE_ID', 'Mean_Throughput', 'Std_Throughput', 'Mean_SE', 'Std_SE']]

  # save
  agg.to_csv(os.path.join(base_output_dir, "agg-" + str(scenario) + "-" + str(rep) + ".csv"), index=False)
  print(f"New file stored in {base_output_dir} for {scenario} \n")


#analysis_per_mean("cb", "1")
#analysis_per_mean("cb", "5")
analysis_per_mean("cb", "10")

#analysis_per_mean("cf", "1")
#analysis_per_mean("cf", "5")
#analysis_per_mean("cf", "10")  