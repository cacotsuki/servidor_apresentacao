from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .funcoes import linux, manipulate_txt,write_sequence, data_visualization,remove_barra,salva_na_pasta_vienna,gera_imagem,executa_shell

from .vienn2 import converte_to_string,abre_arquivo,limpar,get_exec_time
from .vienn2_upload import converte_to_string_upload,abre_arquivo_upload,limpar_upload,get_exec_time_upload,remove_barra_upload,data_visualization2
from .seq_length import seq_len_input
from .forms import Leitor
from .forms import BookForm
from .models import Book
from .roda_upload import linux_upload,le_upload,remove_fasta_apos_execucao,salva_na_pasta_vienna_upload,gera_imagem_upload,converte_e_transfere_upload #arquivo responsavel pro executar o cuda_sankoff pelo upload
from .seq_length_upload import seq_len_upload

class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)




        linux_upload()
        le_upload()
        data_visualization2()
        remove_barra_upload()
        salva_na_pasta_vienna_upload()

        gera_imagem_upload()
        converte_e_transfere_upload()


        

        if seq_len_upload(1) < 41 and seq_len_upload(2) < 41:   
            if seq_len_upload(1) == seq_len_upload(2):             
                return render(request, 'resultado_upload.html',
                            {'read': converte_to_string_upload(limpar_upload(abre_arquivo_upload())), 'exec': get_exec_time_upload(),
                            'seq1_len': seq_len_upload(1), 'seq2_len': seq_len_upload(2),'nada_faz':remove_fasta_apos_execucao()})


        else:
            return render(request, 'mensagem_erro.html')







        
    else:
        return render(request, 'upload.html')


def ferramenta(request):
    if request.method == 'POST':
        form = Leitor(request.POST)
        if form.is_valid():
            text_area = form.cleaned_data['text_area']
            # retorno = linux(text_area)
            # abre_arquivo()
            limpar(abre_arquivo())
            # str(retorno)
            # print(retorno)

            remove_barra()
            # write_sequence(retorno)
            write_sequence(text_area)  # escreve no .fasta a entrada do textarea
            data_visualization()
            # read_sequence()
            linux()  # executa o algoritmo com base no .fasta
            #leitura_upload()  # executa o algoritmo com base no .fasta
            #  read_sequence()
            #executa_shell()
            salva_na_pasta_vienna()
            gera_imagem()    
            executa_shell()        
            get_exec_time()
            manipulate_txt()  # realiza a leitura da saida do algoritmo sankoffAPP
            # converte_to_string(limpar(abre_arquivo()))



            
            if seq_len_input(1) < 41 and seq_len_input(2) < 41 :                
                return render(request, 'result.html',
                        {'read': converte_to_string(limpar(abre_arquivo())), 'exec': get_exec_time(),
                        'seq1_len': seq_len_input(1), 'seq2_len': seq_len_input(2)})
            else:
                return render(request, 'mensagem_erro.html')



    else:
        form = Leitor(request.POST)
    return render(request, 'ferramenta.html', {'form': form})