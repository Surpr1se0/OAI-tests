import pandas as pd
import matplotlib.pyplot as plt
import os

UE_NAME_1 = "ue1"
UE_NAME_2 = "ue2"
UE_NAME_6 = "ue6"

csv_path_1 = os.path.join("pilot-analysis", "clean-files", "dmrs_pdsch", "PDSCH_DMRS" + UE_NAME_1 + ".csv")
csv_path_2 = os.path.join("pilot-analysis", "clean-files", "dmrs_pdsch", "PDSCH_DMRS" + UE_NAME_2 + ".csv")
csv_path_6 = os.path.join("pilot-analysis", "clean-files", "dmrs_pdsch", "PDSCH_DMRS" + UE_NAME_6 + ".csv")

df = pd.read_csv(csv_path_1, sep=",")
df.columns = df.columns.str.strip()
i_part = df['I Part'].astype(int)
q_part = df['Q Part'].astype(int)

df_2 = pd.read_csv(csv_path_2, sep=",")
df_2.columns = df_2.columns.str.strip()
i_part_2 = df_2['I Part'].astype(int)
q_part_2 = df_2['Q Part'].astype(int)

df_6 = pd.read_csv(csv_path_2, sep=",")
df_6.columns = df_6.columns.str.strip()
i_part_6 = df_6['I Part'].astype(int)
q_part_6 = df_6['Q Part'].astype(int)

# print("Valores únicos de I:", i_part_6.unique())
# print("Valores únicos de Q:", q_part_6.unique())
# print("Colunas disponíveis:", df_6.columns)
# print("Primeiras linhas do DataFrame:")
# print(df.head())
# print("\nValores únicos de I Part:", i_part_6.unique())
# print("Valores únicos de Q Part:", q_part_6.unique())

max_val = max(i_part.abs().max(), q_part.abs().max())
i_norm = i_part / max_val
q_norm = q_part / max_val

max_val_2 = max(i_part_2.abs().max(), q_part_2.abs().max())
i_norm_2 = i_part_2 / max_val_2
q_norm_2 = q_part_2 / max_val_2

max_val_6 = max(i_part_6.abs().max(), q_part_6.abs().max())
i_norm_6 = i_part_6 / max_val_6
q_norm_6 = q_part_6 / max_val_6

plt.figure(figsize=(6, 6))
plt.scatter(i_norm, q_norm, color='blue', label= UE_NAME_1, alpha=0.5)
plt.scatter(i_norm_2, q_norm_2, color='red', label= UE_NAME_2, alpha=0.5)
plt.scatter(i_norm_6, q_norm_6, color='green', label= UE_NAME_6, alpha=0.5)
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.grid(True)
plt.title('Constelation PDSCH')
plt.xlabel('I')
plt.ylabel('Q')
plt.axis('equal')
plt.xlim(-1.2, 1.2)
plt.ylim(-1.2, 1.2)

plt.legend() 
plt.show()