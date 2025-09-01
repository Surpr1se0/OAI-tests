🧠 1. Meaning of each LOG_I(PHY, ...)
✅ Line 1 – Transmitted pilots (DMRS)

LOG_I(PHY, "[PDSCH-DMRS pilot] [%d] = (%d, %d)\n", i, pilot[i].r, pilot[i].i);

i: index of the pilot symbol (DMRS) in the pilot[] array

(%d, %d): real (r) and imaginary (i) parts of the locally generated symbol (already conjugated)

🔹 These are the "known" values ​​used in channel estimation.
✅ Line 2 – Received signals before estimation

LOG_I(PHY, "[PDSCH-RX] aarx=%d i=%d rxF = (%d, %d)\n", aarx, i, rxF[i].r, rxF[i].i);

aarx: receive antenna index

i: index in the rxF[] array, which contains the received OFDM signals

rxF[i]: received complex sample (I/Q) of the channel

🔹 These are the actual values ​​received, before multiplication with the pilot.
✅ Lines 3 and 4 – Channel Estimation (dl_ch)

LOG_I(PHY, "[PDSCH-RX]%4d\t%4d\t", dl_ch[idxP * 8 + idxI].r, dl_ch[idxP * 8 + idxI].i);
LOG_I(PHY, "[PDSCH-RX]%2d\n", idxP);

dl_ch[...]: estimated channel response value, after estimation with pilots

idxP: block index (each block usually has 8 samples)

idxI: internal index within the block

🔹 This represents the estimated channel response for each RE (Resource Element).
📊 2. What to export to CSV and why
🔎 Useful data:
Source field Useful for CSV? Reason
pilot[i] line 1 ✅ To confirm consistency with rxF
rxF[i] line 2 ✅ To observe channel impact
aarx line 2 ✅ To separate channels from different antennas
dl_ch[idx] lines 3 and 4 ✅ To verify the final estimate