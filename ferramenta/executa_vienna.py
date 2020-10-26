import re
import subprocess
from matplotlib import pylab

mid = []
novo = []
novo2 = []

def abre_arquivo():
    hamb = []
    lista = []
    with open('/home/ubuntu/ferramenta_final/servidor_apresentacao/cuda_sankoff/ViennaRNA-2.3.3/resultado_cuda_sankoff.txt') as file:
        for line in file:
            hamb.append(line)
    lista.append(hamb[4])
    lista.append(hamb[5])
    lista.append(hamb[6])
    return lista
#print(abre_arquivo())


def limpar(lista):
    lista_limpa = []
    for x in lista:
        item = x
        for y in ['\n', '\t', '/', 't', 'seq', ':', '[', ']', ' ']:
            item = item.replace(y, "")
            item = item.replace(y, "")

        lista_limpa.append(item)
    return lista_limpa

# executa a função limpar, realizando a limpeza na lista proveniente da função abre_arquivo
#print(limpar(abre_arquivo()))

def converte_to_string(lista_limpa):
    lista_string = []
    lista2 = []
    #limpeza = ''.join(str(e) for e in lista_limpa)
    lista_string1 = str(lista_limpa[0])
    lista_string2 = str(lista_limpa[1])
    #final3 = str(lista_string[2])
    lista_final = []

    lista_final.append(re.sub('[0-9]', '', lista_string1))  # REGEX QUE REMOVE TODOS OS NUMEROS INTEIROS DA LISTA)
    b2 = str(novo2)  # precisa chegar aqui como string
    lista_final.append(re.sub('[0-9]', '', lista_string2))  # REGEX QUE REMOVE TODOS OS NUMEROS INTEIROS DA LISTA
    lista_final.append(lista_limpa[2])
    #print('aqui',final1)

    return lista_final


print()


def le_resultado():
    lista = []
    leitura = open('/home/ubuntu/ferramenta_final/servidor_apresentacao/cuda_sankoff/ViennaRNA-2.3.3/resultado_cuda_sankoff.txt')



    with open('/home/ubuntu/ferramenta_final/servidor_apresentacao/cuda_sankoff/ViennaRNA-2.3.3/resultado_cuda_sankoff.txt') as file:
        for line in file:
            lista.append(line)

    return lista

print(le_resultado()[4])
print(le_resultado()[5])




#limpar(le_resultado())


def exe_vi():
    import subprocess

    subprocess.check_output(['./RNAplot_one_seq.sh', 'CCCAAAGGG', '(((...))).'],
                            cwd='/home/ubuntu/ferramenta_final/servidor_apresentacao/cuda_sankoff/ViennaRNA-2.3.3')
exe_vi()
#executa_vienna(limpar(le_resultado()))

