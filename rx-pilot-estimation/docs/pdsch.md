🧠 1. Significado de cada LOG_I(PHY, ...)
✅ Linha 1 – Pilotos (DMRS) transmitidos

LOG_I(PHY, "[PDSCH-DMRS pilot] [%d] = (%d, %d)\n", i, pilot[i].r, pilot[i].i);

    i: índice do símbolo piloto (DMRS) no vetor pilot[]

    (%d, %d): parte real (r) e imaginária (i) do símbolo gerado localmente (já conjugado)

🔹 Estes são os valores "conhecidos" usados na estimação do canal.
✅ Linha 2 – Sinais recebidos antes da estimação

LOG_I(PHY, "[PDSCH-RX] aarx=%d i=%d rxF = (%d,%d)\n", aarx, i, rxF[i].r, rxF[i].i);

    aarx: índice da antena de receção

    i: índice no vetor rxF[], que contém os sinais OFDM recebidos

    rxF[i]: amostra complexa (I/Q) recebida do canal

🔹 Estes são os valores reais recebidos, antes da multiplicação com o piloto.
✅ Linha 3 e 4 – Estimativa de canal (dl_ch)

LOG_I(PHY, "[PDSCH-RX]%4d\t%4d\t", dl_ch[idxP * 8 + idxI].r, dl_ch[idxP * 8 + idxI].i);
LOG_I(PHY, "[PDSCH-RX]%2d\n", idxP);

    dl_ch[...]: valor estimado da resposta ao canal, após estimação com os pilotos

    idxP: índice do bloco (normalmente cada bloco tem 8 amostras)

    idxI: índice interno dentro do bloco

🔹 Isto representa a estimativa da resposta ao canal em cada RE (Resource Element).  
📊 2. O que exportar para CSV e porquê
🔎 Dados úteis:  
Campo	Origem	Útil para CSV?	Motivo  
pilot[i]	linha 1	✅	Para confirmar coerência com rxF  
rxF[i]	linha 2	✅	Para observar o impacto do canal  
aarx	linha 2	✅	Para separar canais de antenas diferentes  
dl_ch[idx]	linha 3 e 4	✅	Para verificar a estimativa final  