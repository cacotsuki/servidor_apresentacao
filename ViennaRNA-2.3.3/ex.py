lista = ['./src/bin/RNAplot','CCCCCCCCAAAAGGGGGGGG','((((((((....))))))))','@']

lista2 = './src/bin/RNAplot ; CCCAAAGGGACCCAAAGGG ; (((...))).(((...))) ; @'
#os.system('./src/bin/RNAplot ; CCCCCCCCAAAAGGGGGGGG ; ((((((((....)))))))) ; @ ;')
import subprocess, shlex
from subprocess import Popen, PIPE, STDOUT

cmd1 = './src/bin/RNAplot'
cmd2 = 'CCCAAAGGGACCCAAAGGG'
cmd3 = '(((...))).(((...)))'
cmd4 = '@'
final = Popen("{}; {}; {}; {}".format(cmd1, cmd2,cmd3,cmd4), shell=True, stdin=PIPE, 
          stdout=PIPE, stderr=STDOUT, close_fds=True)
stdout, nothing = final.communicate()
log = open('log', 'w')
log.write(stdout)
log.close()