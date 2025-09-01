import pandas as pd
import os

df_ue0 = pd.read_csv("rx-pilot-estimation/clean-files/PDSCH/ue1.csv")
df_ue1 = pd.read_csv("rx-pilot-estimation/clean-files/PDSCH/ue6.csv")

pilots_ue0 = df_ue0[df_ue0["type"] == "pilot"].copy()
pilots_ue1 = df_ue1[df_ue1["type"] == "pilot"].copy()

# add ue_id field
pilots_ue0["ue_id"] = 0
pilots_ue1["ue_id"] = 1

# combine both data sets
combined = pd.concat([pilots_ue0, pilots_ue1], ignore_index=True)

# I,Q pairing
grouped = combined.groupby(["I", "Q"])

def has_multiple_ue_ids(group):
    return group["ue_id"].nunique() > 1
duplicates = grouped.filter(has_multiple_ue_ids)


duplicates_sorted = duplicates.sort_values(by=["I", "Q", "ue_id"])
print("Valores de piloto reutilizados entre UEs diferentes:")
print(duplicates_sorted[["ue_id", "index", "I", "Q"]])
duplicates_sorted.to_csv("pilotos_reutilizados.csv", index=False)