import pandas as pd
import os 

# === CONFIGURAÇÃO ===
base_dir_input = os.path.join("mac-throughput" ,"clean-files-ul", "aggr")
CSV_METRICAS = "mac_throughput_log.csv"  # <-- Substituir pelo caminho correto

RNTI_TO_LOGICAL_UE = {
    2: 0,
    3: 0,
    5: 1,
    8: 1,
    10: 1,
}

# === PROCESSAMENTO ===

# Lê o CSV com as métricas da camada MAC
df = pd.read_csv(base_dir_input + CSV_METRICAS)

# Mapeia cada RNTI para o UE lógico correspondente
df['logical_ue'] = df['UE_ID'].map(RNTI_TO_LOGICAL_UE)

# Remove entradas sem mapeamento
df = df.dropna(subset=['logical_ue'])

# Garante que o tipo é inteiro
df['logical_ue'] = df['logical_ue'].astype(int)

# Agrupa por tempo e UE lógico, somando throughput
df_agg = df.groupby(['time_ms', 'logical_ue']).agg(
    total_throughput_mbps=('throughput_mbps', 'sum'),
    num_rntis_ativos=('UE_ID', 'count')
).reset_index()

# Mostra os resultados
print(df_agg)

# Exporta para CSV se quiseres guardar
df_agg.to_csv(base_dir_input + "throughput_aggregado_por_ue_logico.csv", index=False)
