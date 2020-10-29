import subprocess
def seq_len_upload(qual_seq):
    #converte()
    fasta = []
    seq = []
    with open('/home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/media/arquivo.fasta') as file:
        for line in file:
            fasta.append(line)

    for x in fasta:
        item = x
        for y in ['\n', '\t', '/', 'seq', ':', '[', ']', ' ']:
            item = item.replace(y, "")

        seq.append(item)

    if qual_seq == 1:
        exibe = seq[1]
    elif qual_seq == 2:
        exibe = seq[3]

    return len(exibe)




