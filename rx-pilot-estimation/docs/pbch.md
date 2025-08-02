1. pilot[i] = (r, i)

    Refere-se ao símbolo piloto gerado localmente no UE, já conjugado (DMRS*).

    Usado para estimação de canal.

    Valor teórico esperado (por exemplo, em QPSK: ±23170).

2. rxF[re_offset] = (r, i)

    Amostra recebida do canal, no subportador k + re_offset.

    Representa o que o UE recebeu do gNB no recurso onde deveria estar um piloto.

    Contaminado por ruído, canal, distorções.

3. ch = (r, i)

    Resultado da estimação do canal para aquele piloto.

    Calculado com:

    ch.r = pil->r * rxF.r - pil->i * rxF.i;
    ch.i = pil->r * rxF.i + pil->i * rxF.r;

    Representa a resposta ao canal complexa nesse ponto (antes de normalizar/dividir por |piloto|², pois já está conjugado).

4. k, first_carrier

    k: índice do subportador onde a estimativa está a ser feita.

    first_carrier: offset do primeiro subportador em uso, normalmente depende do número de PRBs (RBs).

📄 Formato CSV sugerido
tipo	idx	rxF_r	rxF_i	ch_r	ch_i	pilot_r	pilot_i	k	first_carrier
pbch	0	12	-4	300	220	23170	-23170	1	1412
pbch	1	...	...	...	...	...	...		
...	