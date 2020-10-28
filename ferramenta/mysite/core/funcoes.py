import os
import subprocess
from builtins import print
from os import path
from matplotlib import pylab
from pylab import *
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import GC
import os






# Compila o algoritmo Sankoff a partir de sua localizacao
# Segundo argumento e o mesmo segundo argumento do terminal para compilar
# Escreve no teste.txt a saida do algoritmo
def linux():
    subprocess.check_output(['dos2unix', 'write2.fasta'], cwd='/home/ubuntu/ferramenta_final/cuda_sankoff/seqs' )
    a = subprocess.check_output(['./bin/sankoff', 'seqs/write2.fasta'], cwd='/home/ubuntu/ferramenta_final/cuda_sankoff')
    str(a,'utf-8')

    file = open('resultado_cuda_sankoff.txt', 'w')
    file.write(str(a,'utf-8'))
    file.close()



    return a.decode('utf-8')

def salva_na_pasta_vienna():
    subprocess.check_output(['dos2unix', 'write2.fasta'], cwd='/home/ubuntu/ferramenta_final/cuda_sankoff/seqs')
    a = subprocess.check_output(['./bin/sankoff', 'seqs/write2.fasta'],
                               cwd='/home/ubuntu/ferramenta_final/cuda_sankoff/seqs')
    str(a, 'utf-8')
    vienna = open('/home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/resultado_cuda_sankoff.txt', 'w')
    vienna.write(str(a, 'utf-8'))
    vienna.close()

def gera_imagem():
    subprocess.check_output(['python3', 'gera_imagem.py'],
                             cwd='/home/ubuntu/ferramenta_final/cuda_sankoff/ViennaRNA-2.3.3')
    subprocess.check_output(['./django.sh'],
                            cwd='/home/ubuntu/ferramenta_final/cuda_sankoff/ViennaRNA-2.3.3')

def executa_shell():
    subprocess.check_output(['./copia_para_vienna.sh'],
                             cwd='/home/ubuntu/ferramenta_final/cuda_sankoff/ViennaRNA-2.3.3')





# Grava num .fasta o que foi a entrada texto da home
def write_sequence(text_area):
    wrt = open('/home/ubuntu/ferramenta_final/cuda_sankoff/seqs/write2.fasta', 'w')

    wrt.write(str(text_area))
    wrt.close()

# Realiza a leitura do .fasta o que foi a entrada texto da home
def read_sequence():
    #arch = open('/home/livanski/Documents/danielsundfeld-hpc/seqs/write.fasta','r')
    with open('/home/ubuntu/ferramenta_final/cuda_sankoff/seqs/write2.fasta') as file:
        for line in file:
            line.split('\n')

def remove_barra():
    hamb = []
    novo = []

    with open('/home/ubuntu/ferramenta_final/cuda_sankoff/seqs/write2.fasta') as file:
        for line in file:
            hamb.append(line)

    for x in hamb:
        item = x
        for y in ['l', '\t', '/', '.', '-', '(', '),', 't', 'seq2', ':', ')', '7']:
            item = item.replace(y, "")
        novo.append(item)

#novo é a lista com o fasta limpo
    a = "".join(novo)
    wrt = open('/home/ubuntu/ferramenta_final/cuda_sankoff/seqs/write2.fasta', 'w')
    wrt.write(a)


# Grava num .txt a a saida do algoritmo Sankoff
def create_file():
    file = open('resultado_cuda_sankoff.txt', 'w')
    file.write(str())
    file.close()

# Realiza a leitura do .txt com a saida do algoritmo Sankoff e os coloca em um Array List
def read_file():
   # subprocess.check_output(['dos2unix', 'write.fasta'], cwd='/home/livanski/Documents/danielsundfeld-hpc/seqs')
    #ler = open('teste.txt', 'r')
    ler = open('/home/ubuntu/ferramenta_final/cuda_sankoff/seqs/write2.fasta','r')
    read = ler.readline()
    return read

print(read_file())
# Realiza a leitura linha por linha do .txt
#("\n", "\r\n")
def manipulate_txt():
    # tst = []
    #
    # with open("teste.txt") as file:
    #     for line in file:
    #         tst.append(line)
    #
    meuArquivo = open('resultado_cuda_sankoff.txt', 'r')
    saida_sankoff = meuArquivo.readlines()

    for index in range(len(saida_sankoff)):
        saida_sankoff[index] = saida_sankoff[index].rstrip('\n')

    meuArquivo.close()


    return saida_sankoff



def data_visualization():
    #subprocess.check_output(['dos2unix', 'teste.txt'])



    hamb = []
    #subprocess.check_output(['dos2unix', 'write.fasta'], cwd='/home/livanski/Documents/danielsundfeld-hpc/seqs')
    #with open("teste.txt") as file:
    with open('/home/ubuntu/ferramenta_final/cuda_sankoff/seqs/write2.fasta') as file:
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
    pylab.savefig('/home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/static/graph.png', dpi=100)
    pylab.savefig('/home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/mysite/static/css/graph.png', dpi=100)
    return pylab.show



