import re
import subprocess

mid = []
novo = []
novo2 = []

def abre_arquivo():
    hamb = []
    lista = []
    with open('resultado_cuda_sankoff_upload.txt') as file:
        for line in file:
            hamb.append(line)
    lista.append(hamb[4])
    lista.append(hamb[5])    
    return lista



def limpar(lista):
 lista_limpa = []
 for x in lista:
        item = x
        for y in ['\n', '\t', '/', 'seq', ':', '[', ']', ' ']:
            item = item.replace(y, "")

        lista_limpa.append(item)
 return lista_limpa

# executa a função limpar, realizando a limpeza na lista proveniente da função abre_arquivo
#print(limpar(abre_arquivo()))

#print(limpar(abre_arquivo()))


#converte_to_string(limpar(abre_arquivo))



def exe_vi(lista_final):    
    seq1 = lista_final[0]
    seq2 = lista_final[1]
    subprocess.check_output(['./RNAplot_one_seq.sh', seq1, seq2],
                            cwd='/home/ubuntu/ferramenta_final/cuda_sankoff/ViennaRNA-2.3.3')


#exe_vi((limpar(abre_arquivo()))

exe_vi(limpar(abre_arquivo()))