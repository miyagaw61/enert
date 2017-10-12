#       enert - miyagaw61's python library
#
#       Copyright (C) 2017 Taisei Miyagawa <Twitter: @miyagaw61, WebPage: miyagaw61.github.io>
#
#       License: MIT

import os, sys, subprocess, re, binascii
from .init import *
from .toplevel import *
from collections import OrderedDict
#import datetime
#import better_exceptions

if python3:
    from .argparse import *

class File:
    def __init__(self, file_name):
        self.name = file_name

    def name(self):
        return self.name

    def data(self):
        if os.path.exists(self.name):
            try:
                data = open(self.name).read()
            except:
                data = open(self.name, 'rb').read()
            return data
        else:
            return ''
    
    def binary(self):
        if os.path.exists(self.name):
            data = open(self.name, 'rb').read()
            data = dmp(data)
            return data

    def linedata(self):
        if os.path.exists(self.name):
            linedata = open(self.name).readlines()
            for i in range(len(linedata)):
                linedata[i] = regex_n.sub('', linedata[i])
            return linedata
        else:
            return ''

    def white_data(self):
        regex_color = re.compile(r'\x1b.*?m')
        if os.path.exists(self.name):
            data = open(self.name).read()
            return regex_color.sub('', data)
        else:
            return ''

    def white_linedata(self):
        regex_color = re.compile(r'\x1b.*?m')
        if os.path.exists(self.name):
            linedata = open(self.name).readlines()
            for i in range(len(linedata)):
                linedata[i] = regex_n.sub('', linedata[i])
                linedata[i] = regex_color.sub('', linedata[i])
            return linedata
        else:
            return ''

    def lines(self):
        if os.path.exists(self.name):
            return len(self.linedata())
        else:
            return ''

    def write(self, data):
        fd = open(self.name, 'w')
        fd.write(data)
        fd.close()

    def add(self, data):
        fd = open(self.name, 'a')
        fd.write(data)
        fd.close()

    def exist(self):
        return os.path.exists(self.name)

    def rm(self):
        if os.path.exists(self.name):
            os.unlink(self.name)

    def edit(self):
        editor = 'vi'
        if os.environ['EDITOR']:
            editor = os.environ['EDITOR']
        cmd = [editor, 
                self.name]
        subprocess.call(cmd)

class Shell:
    def __init__(self, cmd):
        self.cmd = cmd

    def data(self):
        proc = subprocess.Popen(
                self.cmd,
                shell  = True,
                stdin  = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        stdout_str, stderr_str = proc.communicate()
        if type(stdout_str) == bytes:
            stdout_str = stdout_str.decode()
        if type(stderr_str) == bytes:
            stderr_str = stderr_str.decode()
        return [stdout_str, stderr_str]

    def call(self):
        #os.system(self.cmd)
        proc = subprocess.Popen(
                self.cmd,
                shell  = True)
        proc.communicate()

    def linedata(self):
        stdout_str, stderr_str = self.data()
        f = fl('/tmp/enert.tmp')
        f.write(stdout_str)
        linedata = []
        linedata.append(f.linedata())
        f.write(stderr_str)
        linedata.append(f.linedata())
        f.rm()
        return linedata

esc = '\033'
csi = esc + '['
def to(n=1):
    sys.stdout.write(csi + str(n) + 'G')
    sys.stdout.flush()

def all_delete():
    sys.stdout.write(csi + '2K')
    sys.stdout.write(csi + '1G')
    sys.stdout.flush()

def n2tail_delete(n):
    to(str(n))
    sys.stdout.write(csi + '0K')
    sys.stdout.write(csi + '1G')
    sys.stdout.flush()

def head2n_delete(n):
    to(str(n))
    sys.stdout.write(csi + '1K')
    sys.stdout.write(csi + '1G')
    sys.stdout.flush()

def down(n=1):
    sys.stdout.write(csi + str(n) + 'B')
    sys.stdout.flush()

def up(n=1):
    sys.stdout.write(csi + str(n) + 'A')
    sys.stdout.flush()

def overwrite(strings):
    sys.stdout.write('\r')
    sys.stdout.write(strings)

def save():
    sys.stdout.write(csi + 's')
    sys.stdout.flush()

def restore():
    sys.stdout.write(csi + 'u')
    sys.stdout.flush()

def lines_delete(n):
    sys.stdout.write(csi + str(n) + 'M')

def get_term_size():
    return map(int, os.popen('stty size').read().split())

def clear():
    shell('clear').call()

def writefile(buf_arg,file_name):
    with open(file_name, 'wb') as f:
        f.write(buf_arg)

def addr2index(x):
    return x*2

def index2addr(x):
    return x/2

def ascii2addr(x):
    addr1 = str(x)[0:2]
    addr2 = str(x)[2:4]
    addr3 = str(x)[4:6]
    addr4 = str(x)[6:8]
    return int(addr4 + addr3 + addr2 + addr1, 16)

def splitn(data, n):
    """
        Usage: splitn(str data, int n)
    """
    length = len(data)
    return [data[i:i+n] for i in range(0, length, n)]

def diff(a, b):
    if a > b:
        return a - b
    else:
        return b - a

def dmp(binary, fmt=None):
    """
        Usage: dmp(bin binary, split=''/'x'/'d')
    """
    res = binascii.hexlify(binary)
    if type(res) == bytes:
        res = str(res)[2:-1]
    if(fmt != None):
        arr = splitn(res, fmt)
        res = []
        for var in arr:
            res.append(ascii2addr(var.decode()))
    return res

def complement(value, s):
    """
        Usage: complement(int value, int s)
    """
    value_str = bin(value)[2:].zfill(s)
    if(value_str[0] == '0'):
        return value
    else:
        value = value - 1
        value = value ^ 2**s-1
        return 0-value

def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class Screen():
    def __init__(self):
        save()

    def addstr(self, x, y, strings):
        restore()
        down(y)
        to(x)
        sys.stdout.write(strings)
        restore()

    def overwrite(self, x, y, strings):
        restore()
        down(y)
        to(x)
        all_delete()
        sys.stdout.write(strings)
        restore()

class Menu():
    def __init__(self, lst, function):
        self.i = 0
        self.lst = lst
        self.num = len(lst)
        self.function = function
        self.top = blue('>', 'bold') + '  '
        self.to = 3

    def menu_exit(self):
        restore()
        to(1)
        lines_delete(100)

    def menu_start(self):
        sys.stdout.write(self.top)
        print('')
        for self.i in range(self.num):
            if self.i == 0:
                print(black_red('> ', 'bold') + black_white(self.lst[self.i], 'bold'))
            else:
                print(black_white(' ') +  ' ' + self.lst[self.i])
        self.i = 0
        up(self.num+1)
        save()
        to(self.to)
        while 1:
            key = getch()
            restore()
            sys.stdout.write(self.top)
            to(self.to)
            if (key == 'j' or ord(key) == DOWN) and self.i < self.num-1:
                down(self.i+1)
                all_delete()
                overwrite(black_white(' ') + ' ' + self.lst[self.i])
                restore()
                down(self.i+2)
                overwrite(black_red('> ', 'bold') + black_white(self.lst[self.i+1], 'bold'))
                restore()
                to(3)
                self.i = self.i + 1
            if (key == 'k' or ord(key) == UP) and self.i >= 1:
                down(self.i+1)
                all_delete()
                overwrite(black_white(' ') + ' ' + self.lst[self.i])
                restore()
                down(self.i)
                overwrite(black_red('> ', 'bold') + black_white(self.lst[self.i-1], 'bold'))
                restore()
                to(3)
                self.i = self.i -1
            elif key == 'q' or ord(key) == CTRL_C or ord(key) == CTRL_D:
                self.menu_exit()
                exit()
            elif ord(key) == ENTER:
                self.function(self.i)

def parse_usage(usage, args):
    """
    Usage: parse_usage(usage, args)
    Example usage: 'git [commit <-m>] [push <branch>]'
    Example args: ['commit [-m <comment>]:commit to local repository', 'push [branch]:push to remote repository']
    """
    argparser = ArgumentParser(usage=usage)
    for x in args:
        argparser.add_argument(x.split(':')[0], type=str, help=x.split(':')[1])
    tmp_args = argv
    tmp_args.append('-h')
    args = argparser.parse_args(tmp_args)

def list_check(listA, listB):
    """
    a = [1, 2, 3]
    b = [4, 5, 6]
    list_check(a, b) == 0
    b = [3, 4, 5]
    list_check(a, b) == 1
    """
    ans = 0
    for A in listA:
        for B in listB:
            if A == B:
                ans = 1
    return ans

def help_check(lst, idx=None):
    """
    Usage: help_check()
    Usage: help_check(lst, idx)
    Example: help_check(argv[2:]) #check argv[2:] in '-h' or '--help'
    Example: help_check(argv[2:], 3) # check argc < 3
    """
    if '-h' in argv or '--help' in argv:
        return 1
    else:
        if idx:
            if argc < idx:
                return 1
            else:
                return 0
        else:
            return 0

def select_input(strings, lst):
    while 1:
        ans = input(strings)
        if ans in lst:
            break
    return ans

def list_print(lst):
    for x in lst:
        print(x)

def b():
    import pdb
    pdb.set_trace()

def inf(data, prefix=None, c='green'):
    if prefix == None:
        prefix = '['+red('+','bold')+']'
    else:
        prefix = red(prefix, 'bold')
    term_y, term_x = get_term_size()
    if c == 'green':
        print(green('\n' + '='*term_x, 'bold'))
        sys.stdout.write(prefix)
        print(data)
        print(green('='*term_x + '\n', 'bold'))
    if c == 'red':
        print(red('\n' + '='*term_x, 'bold'))
        sys.stdout.write(prefix)
        print(data)
        print(red('='*term_x + '\n', 'bold'))
    if c == 'blue':
        print(blue('\n' + '='*term_x, 'bold'))
        sys.stdout.write(prefix)
        print(data)
        print(blue('='*term_x + '\n', 'bold'))

def calc(args=None, cmd=False):
    """
    Usage:
    calc('0xa') -> 10
    calc('10 x') -> 0xa
    calc('10 b') -> 0b1010
    calc('5/3') -> 1.5
    """
    if args:
        tmp = args.split(' ')
        args = ['calc']
        for x in tmp:
            args.append(x)
    else:
        args = sys.argv
    argc = len(args)

    if(args[1] == '-h'):
        print('Usage: calc [x/b/i] [expr]')
        exit()

    regex_ipt = re.compile(r'(.*) (.*)')

    if('i' in args):
        while(True):
            sys.stdout.write(green('(calc)$ ', 'bold'))
            ipt_data = input()
            ipt = regex_ipt.findall(ipt_data)
            if not(ipt):
                ipt = ipt_data
                ln = 1
                exp = ipt
            else:
                ipt = ipt[0]
                ln = len(ipt)
                if(ln == 1):
                    exp = ipt[0]
                else:
                    if(len(ipt[0]) == 1): 
                        fmt = ipt[0]
                        exp = ipt[1]
                    else:
                        exp = ipt[0]
                        fmt = ipt[1]
            if(ln == 1):
                if(exp == 'q' or exp == 'exit'):
                    exit()
                else:
                    if cmd:
                        exec('print(' + exp + ')')
                    else:
                        return str(eval(exp))
            else:
                if(fmt.count('x') > 0):
                    if cmd:
                        exec('print(hex(' + exp + '))')
                    else:
                        var = eval(exp)
                        return hex(var)
                elif(fmt.count('b') > 0):
                    if cmd:
                        exec('print(bin(' + exp + '))')
                    else:
                        var =  eval(exp)
                        return bin(var)
    elif('x' in args):
        fmtindex = args.index('x')
        if(fmtindex == 1):
            exp = args[2]
        else:
            exp = args[1]
        if cmd:
            exec('print(hex(' + exp + '))')
        else:
            var = eval(exp)
            return hex(var)
        exit()
    elif('b' in args):
        fmtindex = args.index('b')
        if(fmtindex == 1):
            exp = args[2]
        else:
            exp = args[1]
        if cmd:
            exec('print(bin(' + exp + '))')
        else:
            var = eval(exp)
            return bin(var)
    else:
        exp = args[1]
        if('f' in args):
            if cmd:
                exec('print(1.0*' + exp + ')')
            else:
                return str(eval('1.0*' + exp))
        else:
            if cmd:
                exec('print(' + exp + ')')
            else:
                var = eval(exp)
                return str(var)

def calc_command():
    calc(args=None, cmd=True)

Fl = File
fl = File
shell = Shell
screen = Screen
menu = Menu

def list_uniq(lst):
    lst_uniq = []
    for x in lst:
        if x not in lst_uniq:
            lst_uniq.append(x)
    return lst_uniq

class enerdict(dict):
    def __init__(self, **kwargs):
        self._dict = dict(kwargs)
        key_lst = list(kwargs)
        lst = []
        for key in key_lst:
            lst.append([key, self._dict[key]])
        self.list = lst
        self.keys = list(self._dict.keys())
        self.values = list(self._dict.values())

    def __str__(self):
        return repr(self._dict)

    def __repr__(self):
        return repr(self._dict)

    def __setitem__(self, key, value):
        self._dict[key] = value

    def append(self, *args, **kwargs):
        if len(args) > 1:
            key = args[0]
            value = args[1]
            self._dict[key] = value
        elif len(kwargs) > 0:
            for key in kwargs:
                self._dict[key] = kwargs[key]

def search(arg, out=False):
    lst,err = Shell("find -type f").linedata()
    length_str = str(len(lst))
    result = []
    for i in range(len(lst)):
        f = File(lst[i])
        data = f.data()
        if type(data) == bytes:
            data = dmp(data)
        if i%100 == 0:
            if out:
                if type(f.data()) == bytes:
                    if len(data) > 50:
                        inf(data[:50], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                    elif len(data) > 5:
                        inf(data[:5], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                    elif len(data) > 0:
                        inf(data[:1], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                    elif len(data) == 0:
                        inf(blue('None', 'bold'), '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                else:
                    if len(data) > 50:
                        tmp = data[:50]
                        if tmp.count('\n') > 0:
                            tmp = regex_before_n.findall(tmp)[0]
                    elif len(data) == 0:
                        tmp = blue('None', 'bold')
                    inf(tmp, '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
        if data.count(arg) > 0:
            result.append(lst[i])

    if out:
        output = ''
        for x in result:
            output += x + '\n'
        inf(output, '[+]RESULT:\n')

    return result

def search_binary(arg, out=False):
    lst,err = Shell("find -type f").linedata()
    length_str = str(len(lst))
    result = []
    for i in range(len(lst)):
        f = File(lst[i])
        data = f.binary()
        if i%100 == 0:
            if out:
                if len(data) > 100:
                    inf(data[:100], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                elif len(data) > 50:
                    inf(data[:50], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                elif len(data) > 5:
                    inf(data[:5], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                elif len(data) > 0:
                    inf(data[:1], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                elif len(data) == 0:
                    inf(blue('None', 'bold'), '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
        if data.count(arg) > 0:
            result.append(lst[i])

    if out:
        output = ''
        for x in result:
            output += x + '\n'
        inf(output, '[+]RESULT:\n')

    return result

def to_ascii(arg):
    result = ''
    for x in arg:
        result += hex(ord(x))[2:]
    return result

#def get_now():
#    now = datetime.datetime.now() 
#    year = str(now.year)[2:]
#    month = '{0:02d}'.format(now.month)
#    day = '{0:02d}'.format(now.day)
#    hour = '{0:02d}'.format(now.hour)
#    minute = '{0:02d}'.format(now.minute)
#    second = '{0:02d}'.format(now.second)
#    return enerdict(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
