import pandas as pd
import matplotlib.pyplot as plt

input_file = "rx-pilot-estimation/clean-files/PDSCH/ue1.csv"
df = pd.read_csv(input_file, header=None, names=["type", "index", "I", "Q", "extra"])
df = df.drop(columns=["extra"])  # remover se não for necessário

# Separar os dois tipos
df_rxF = df[df["type"] == "rxF"]
df_pilot = df[df["type"] == "pilot"]

# Ver alguns exemplos
print(df_rxF.head())
print(df_pilot.head())


plt.figure(figsize=(6,6))
plt.scatter(df_rxF["I"], df_rxF["Q"], color="blue", label="rxF")
plt.scatter(df_pilot["I"], df_pilot["Q"], color="red", marker='x', label="pilots")
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.grid(True)
plt.axis('equal')
plt.title("Constelação PDSCH (rxF vs Pilotos)")
plt.xlabel("I")
plt.ylabel("Q")
plt.legend()
plt.show()