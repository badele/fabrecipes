import shlex
import subprocess
from subprocess import PIPE

def executeCommand(cmd):
    cmdargs = shlex.split(cmd)
    p = subprocess.Popen(cmdargs, stdout=PIPE, stderr=PIPE)
    output, errors = p.communicate()
    if p.returncode:
        print('Failed running %s' % cmd)
        raise Exception(errors)
    return output.decode('utf-8')
