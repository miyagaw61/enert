import os
import sys
import re
import subprocess

argv = sys.argv
argc = len(argv)
regex_n = re.compile(r'\n')
regex_before_n = re.compile(r'(.*?)\n')
regex_s = re.compile(r' ')
regex_blankline = re.compile(r'^$')

ENTER = 13
SPACE = 32
UP = 65
DOWN = 66
LEFT = 68
RIGHT = 67
CTRL_C = 3
CTRL_D = 4
CTRL_J = 10
CTRL_K = 11
CTRL_H = 8
CTRL_L = 12
CTRL_S = 19

try:
    if xrange:
        python3 = False
        python2 = True
        PYTHON3 = False
        PYTHON2 = True
except:
    python3 = True
    python2 = False
    PYTHON3 = True
    PYTHON2 = False

if PYTHON2:
    input = raw_input

proc = subprocess.Popen(
        'chcp',
        shell  = True,
        stdin  = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
stdout_str, stderr_str = proc.communicate()
if len(stderr_str) == 0:
    OS = 'windows'
    os.system('')
else:
    OS = 'linux'

proc = subprocess.Popen(
        'uname -a',
        shell  = True,
        stdin  = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
stdout_str, stderr_str = proc.communicate()
if type(stdout_str) == bytes:
    stdout_str = stdout_str.decode()
if type(stderr_str) == bytes:
    stderr_str = stderr_str.decode()
uname = stdout_str

if uname.count('x86_64') > 0:
    arch = 64
    arch_str = 'amd64'
    ARCH = 64
    ARCH_STR = 'amd64'
else:
    arch = 32
    arch_str = 'i386'
    ARCH = 32
    ARCH_STR = 'i386'
