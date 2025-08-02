✅ 1. Significado dos campos nos logs do PDCCH
A) Pilotos brutos:

LOG_I(PHY, "[PDCCH-DMRS pilot] [%d] = (%d, %d)\n", i, ((c16_t*)pilot)[i].r, ((c16_t*)pilot)[i].i);

    i: índice do piloto (dentro do vetor de pilotos)

    (%d, %d): valores reais e imaginários do piloto (normalmente QPSK com ±23170)

B) Estimativas com multiplicação (estimação de canal ch):

LOG_I(PHY, "[PDCCH] ch 0 %d\n", ((int32_t)pil[0]*rxF[0] - (int32_t)pil[1]*rxF[1]));

    Apenas parte real da estimativa do canal (Re[ch]), calculada diretamente

    Versão mais completa aparece a seguir.

C) Piloto + amostra + resultado da estimação

LOG_I(PHY, "[PDCCH] pilot 0 : rxF - > (%d,%d) addr %p  ch -> (%d,%d), pil -> (%d,%d)\n", rxF[0], rxF[1], &rxF[0], ch[0], ch[1], pil[0], pil[1]);

    rxF: amostra recebida na subportadora (I/Q)

    addr: endereço (podes ignorar)

    ch: estimativa de canal (resultado da multiplicação complexa pilot*rxF)

    pil: valor do piloto nessa RE (subportadora)

Repetido para os outros dois:

LOG_I(PHY, "[PDCCH] pilot 1 : rxF - > (%d,%d) ch -> (%d,%d), pil -> (%d,%d)\n", ...);
LOG_I(PHY, "[PDCCH] pilot 2 : rxF - > (%d,%d) ch -> (%d,%d), pil -> (%d,%d)\n", ...);

D) Dentro de loop:

LOG_I(PHY, "[PDCCH] pilot %u : rxF - > (%d,%d) ch -> (%d,%d), pil -> (%d,%d)\n", pilot_cnt, ...);

    pilot_cnt: índice absoluto dentro do loop de 3xN pilots

    Os restantes campos iguais.

E) Última forma:

LOG_I(PHY, "[PDCCH] pilot[%u] = (%d, %d)\trxF[%d] = (%d, %d)\n", pilot_cnt, pil[0], pil[1], k+1, rxF[0], rxF[1]);

    Forma mais direta, sem estimativa de canal ch.

    Apenas piloto, rxF e subportadora k+1.

📄 CSV sugerido para PDCCH

idx,rxF_r,rxF_i,ch_r,ch_i,pilot_r,pilot_i,k

Se não houver k nos logs diretamente, podemos ignorar ou estimar com base no avanço de 4 subportadoras por RE (padrão NR para DMRS em PDCCH).