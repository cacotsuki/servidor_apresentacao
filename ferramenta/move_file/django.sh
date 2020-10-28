#!/bin/sh
convert -density 300 rna.ps -quality 90 -colorspace RGB rna_convertido.png ; cp /home/ubuntu/cuda_sankoff/ViennaRNA-2.3.3/rna_convertido.png /home/ubuntu/ferramenta_final/servidor_apresentacao/ferramenta/mysite/static/css/rna_convertido.png ; 
