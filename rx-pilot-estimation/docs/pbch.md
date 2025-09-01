1. pilot[i] = (r, i)

Refers to the pilot symbol generated locally at the UE, already conjugated (DMRS*).

Used for channel estimation.

Theoretical expected value (e.g., in QPSK: ±23170).

2. rxF[re_offset] = (r, i)

Sample received from the channel, on subcarrier k + re_offset.

Represents what the UE received from the gNB on the resource where a pilot should be.

Contaminated by noise, channel, and distortions.

3. ch = (r, i)

Result of channel estimation for that pilot.

Calculated with:

ch.r = pil->r * rxF.r - pil->i * rxF.i;

ch.i = pil->r * rxF.i + pil->i * rxF.r;

Represents the complex channel response at that point (before normalizing/dividing by |pilot|², since it is already conjugate).

4. k, first_carrier

k: index of the subcarrier where the estimation is being made.

first_carrier: offset of the first subcarrier in use, usually dependent on the number of PRBs (RBs).

📄 Suggested CSV format
type idx rxF_r rxF_i ch_r ch_i pilot_r pilot_i k first_carrier
pbch 0 12 -4 300 220 23170 -23170 1 1412
pbch 1 ... ... ... ... ... ...
...