import pandas as pd
import os

# Carregar os dois CSVs
df_ue0 = pd.read_csv("rx-pilot-estimation/clean-files/PDSCH/ue1.csv")
df_ue1 = pd.read_csv("rx-pilot-estimation/clean-files/PDSCH/ue6.csv")

# Filtrar apenas os pilotos
pilots_ue0 = df_ue0[df_ue0["type"] == "pilot"].copy()
pilots_ue1 = df_ue1[df_ue1["type"] == "pilot"].copy()

# Adicionar campo ue_id
pilots_ue0["ue_id"] = 0
pilots_ue1["ue_id"] = 1

# Juntar os dois dataframes
combined = pd.concat([pilots_ue0, pilots_ue1], ignore_index=True)

# Agrupar por valor de (I, Q)
grouped = combined.groupby(["I", "Q"])

# Filtrar valores que ocorrem em mais de um UE (i.e., reutilizados)
def has_multiple_ue_ids(group):
    return group["ue_id"].nunique() > 1

duplicates = grouped.filter(has_multiple_ue_ids)

# Ordenar para leitura fácil
duplicates_sorted = duplicates.sort_values(by=["I", "Q", "ue_id"])

# Mostrar resultados
print("Valores de piloto reutilizados entre UEs diferentes:")
print(duplicates_sorted[["ue_id", "index", "I", "Q"]])

# (Opcional) Exportar para CSV
duplicates_sorted.to_csv("pilotos_reutilizados.csv", index=False)