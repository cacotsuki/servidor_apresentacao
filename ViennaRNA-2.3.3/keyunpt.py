import subprocess


#lista = ['./src/bin/RNAplot;CCCCCCCCCCCCCCCC;(((((......)))));@;']
#subprocess.check_output('./src/bin/RNAplot;CCCCCCCCCCCCCCCC;(((((......)))));@;',
#	cwd='/home/livanski/Downloads/ViennaRNA-2.3.3' )

#subprocess.Popen('./src/bin/RNAplot;CCCCCCCCCCCCCCCC;(((((......)))));@;', shell=True)

#result = subprocess.run('./src/bin/RNAplot;CCCCCCCCCCCCCCCC;(((((......)))));@;', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

result = subprocess.run('./src/bin/RNAplot','\n','CCCCCCCCCCCCCCCC','\n','(((((......)))))','\n','@','\n', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
