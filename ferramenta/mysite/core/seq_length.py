def seq_len_input(lista):
    fasta = []
    exibe = 0
    with open('/home/livanski/Music/seq_maior/servidor_apresentacao/ferramenta/resultado_cuda_sankoff.txt') as file:
        for line in file:
            fasta.append(line)



    lista_limpa = []
    for x in fasta:
        item = x
        for y in ['\n', '\t', '/', 't', 'seq1','seq2','A','C','G','U', ':', '[', ']','(',')']:
            item = item.replace(y, "")
            item = item.replace(y, "")

        lista_limpa.append(item)

    if lista == 1:
        exibe = lista_limpa[1]
    elif lista == 2:
        exibe = lista_limpa[2]
    
    return int(exibe)



print(seq_len_input(2))




def confere():
    fasta = []
    seq = []
    with open('/home/livanski/Music/seq_maior/cuda_sankoff/seqs/008.fasta') as file:
        for line in file:
            fasta.append(line)

    for x in fasta:
        item = x
        for y in ['\n', '\t', '/', 'seq', ':', '[', ']', ' ']:
            item = item.replace(y, "")

        seq.append(item)

        