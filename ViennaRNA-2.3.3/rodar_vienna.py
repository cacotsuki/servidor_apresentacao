import subprocess
import os
 
#lista = ['./src/bin/RNAplot','\n','CCCCCCCCAAAAGGGGGGGG','\n','((((((((....))))))))','\n','@','\n']
lista = ['./src/bin/RNAplot','CCCCCCCCAAAAGGGGGGGG','((((((((....))))))))','@']

#a = subprocess.check_output(['./src/bin/RNAplot','CCCCCCCCAAAAGGGGGGGG','\n','((((((((....))))))))','\n','@','\n'], cwd='/home/livanski/Downloads/ViennaRNA-2.3.3')


comando = " ./src/bin/RNAplot ; CCCCCCCCAAAAGGGGGGGG ; ((((((((....)))))))) ; @"

subprocess.check_output(['./src/bin/RNAplot','CCCCCCCCAAAAGGGGGGGG\n','((((((((....))))))))\n','@\n'], cwd='/home/livanski/Downloads/ViennaRNA-2.3.3')