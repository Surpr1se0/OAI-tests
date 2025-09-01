✅ 1. Meaning of the fields in the PDCCH logs
A) Raw pilots:

LOG_I(PHY, "[PDCCH-DMRS pilot] [%d] = (%d, %d)\n", i, ((c16_t*)pilot)[i].r, ((c16_t*)pilot)[i].i);

i: pilot index (within the pilot array)

(%d, %d): real and imaginary pilot values ​​(typically QPSK with ±23170)

B) Estimates with multiplication (ch channel estimation):

LOG_I(PHY, "[PDCCH] ch 0 %d\n", ((int32_t)pil[0]*rxF[0] - (int32_t)pil[1]*rxF[1]));

Only the real part of the channel estimate (Re[ch]), calculated directly.

A more complete version appears below.

C) Pilot + sample + estimation result

LOG_I(PHY, "[PDCCH] pilot 0 : rxF -> (%d,%d) addr %p ch -> (%d,%d), pil -> (%d,%d)\n", rxF[0], rxF[1], &rxF[0], ch[0], ch[1], pil[0], pil[1]);

rxF: received sample on subcarrier (I/Q)

addr: address (you can ignore)

ch: channel estimate (result of complex multiplication pilot*rxF)

pil: pilot value on this RE (subcarrier)

Repeated for the other two:

LOG_I(PHY, "[PDCCH] pilot 1 : rxF -> (%d,%d) ch -> (%d,%d), pil -> (%d,%d)\n", ...);
LOG_I(PHY, "[PDCCH] pilot 2 : rxF -> (%d,%d) ch -> (%d,%d), pil -> (%d,%d)\n", ...);

D) Inside the loop:

LOG_I(PHY, "[PDCCH] pilot %u : rxF -> (%d,%d) ch -> (%d,%d), pil -> (%d,%d)\n", pilot_cnt, ...);

pilot_cnt: absolute index inside the 3xN pilot loop

All other fields are the same.

E) Last form:

LOG_I(PHY, "[PDCCH] pilot[%u] = (%d, %d)\trxF[%d] = (%d, %d)\n", pilot_cnt, pil[0], pil[1], k+1, rxF[0], rxF[1]);

Most direct form, without ch channel estimation.

Only pilot, rxF, and k+1 subcarrier.

📄 Suggested CSV for PDCCH

idx,rxF_r,rxF_i,ch_r,ch_i,pilot_r,pilot_i,k

If k is not directly present in the logs, we can ignore it or estimate it based on advancing 4 subcarriers per RE (NR standard for DMRS on PDCCH).