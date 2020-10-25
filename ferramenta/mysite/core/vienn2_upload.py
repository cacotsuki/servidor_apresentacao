import re
import subprocess
from builtins import print
from os import path
from matplotlib import pylab
from pylab import *
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import GC



mid = []
novo = []
novo2 = []

def abre_arquivo_upload():
    seq1 = []
    seq2 = []
    seq_mid = []
    hamb = []
    lista = []
    with open('/home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/resultado_cuda_sankoff_upload.txt') as file:
        for line in file:
            hamb.append(line)
    lista.append(hamb[4])
    lista.append(hamb[5])
    lista.append(hamb[6])
    return lista
#print(abre_arquivo())


def limpar_upload(lista):
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

def converte_to_string_upload(lista_limpa):
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
#print(converte_to_string(limpar(abre_arquivo())))


#b = str(novo) #precisa chegar aqui como string
'''
def remove_int():
    final1 = re.sub('[0-9]', '', final1) #REGEX QUE REMOVE TODOS OS NUMEROS INTEIROS DA LISTA
    b2 = str(novo2) #precisa chegar aqui como string
    final2 = re.sub('[0-9]', '', final2) #REGEX QUE REMOVE TODOS OS NUMEROS INTEIROS DA LISTA
'''


#a = str(b).strip('[]')


def get_exec_time_upload():
    ex = []
    exec_time = []
    exec_limpo = []
    with open('/home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/resultado_cuda_sankoff_upload.txt') as file:
        for line in file:
            ex.append(line)
    exec_time = ex[8]

    #a = str(exec_time)
    return exec_time

def remove_barra_upload():
    hamb = []
    novo = []

    with open('/home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/media/arquivo.fasta') as file:
        for line in file:
            hamb.append(line)

    for x in hamb:
        item = x
        for y in ['l', '\t', '/', 't', 'seq2', ':']:
            item = item.replace(y, "")
        novo.append(item)
''"""''
print(final1)
# 123



print(final1)

print("------ VERSAO FINAL --------")
print("SEQ1:",final1) #SEQ1 FULL LIMPA
print("SEQ2:",final2) #SEQ2 FULL LIMPA
print("ESTRUTURA SECUNDARIA DE RNA:" ,rna)

"""

def data_visualization2():
    #subprocess.check_output(['dos2unix', 'teste.txt'])



    hamb = []
    #subprocess.check_output(['dos2unix', 'write.fasta'], cwd='/home/livanski/Documents/danielsundfeld-hpc/seqs')
    #with open("teste.txt") as file:
    with open('/home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/media/arquivo.fasta') as file:
        for line in file:
            hamb.append(line)

    seq1 = Seq(hamb[1])
    seq2 = Seq(hamb[3])
    seq3 = seq1 + seq2


    gc = GC(seq3)

    au = 100 - gc

    pylab.pie([gc, au])  # cria o grafico pizza
    pylab.title('GC Content')  # indica um titulo
    pylab.xlabel('GC: %0.1f\nAT: %01.f' % (gc, au))  # porcentagens/info
     # exibe
    #pylab.savefig('/home/livanski/Pictures/graph.png', dpi=100)
    #pylab.savefig('/home/livanski/Music/upload_final/django-upload-example/static/graph.png', dpi=100)
    pylab.savefig('/home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/mysite/static/css/graph_upload.png', dpi=100)
    return pylab.show