#       enert - miyagaw61's python library
#
#       Copyright (C) 2017 Taisei Miyagawa <Twitter: @miyagaw61, WebPage: miyagaw61.github.io>
#
#       License: MIT

import os, sys, subprocess, re, binascii, fcntl, termios

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

class file:
    def __init__(self, file_name):
        self.name = file_name

    def name(self):
        return self.name

    def data(self):
        return open(self.name).read()
    
    def linedata(self):
        return open(self.name).readlines()

    def lines(self):
        return len(self.linedata())

    def write(self, data):
        fd = open(self.name, "w")
        fd.write(data)
        fd.close()

    def add(self, data):
        fd = open(self.name, "a")
        fd.write(data)
        fd.close()

    def exist(self):
        return os.path.exists(self.name)

    def rm(self):
        os.unlink(self.name)

    def edit(self):
        editor = "vi"
        if os.environ["EDITOR"]:
            editor = os.environ["EDITOR"]
        cmd = [editor, 
                self.name]
        subprocess.call(cmd)

    def binary(self, fmt="default"):
        binary_data = open(self.name, "rb").read()
        return dmp(binary_data, fmt)

class shell:
    def __init__(self, cmd):
        self.cmd = cmd

    def get(self):
        proc = subprocess.Popen(
                self.cmd,
                shell  = True,
                stdin  = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        stdout_str, stderr_str = proc.communicate()
        #if type(stdout_str) == bytes:
        #    stdout_str = stdout_str.decode()
        #if type(stderr_str) == bytes:
        #    stderr_str = stderr_str.decode()
        return [stdout_str, stderr_str]

    def call(self):
        os.system(self.cmd)

def colorize(text, color=None, attrib=None):
    # ansicolor definitions
    COLORS = {"black": "30", "red": "31", "green": "32", "yellow": "33",
            "blue": "34", "purple": "35", "cyan": "36", "white": "37", 
            "black_white": "40;37", "black_red": "40;31", "black_green": "40;32"}
    CATTRS = {"regular": "0", "bold": "1", "underline": "4", "strike": "9",
                "light": "1", "dark": "2", "invert": "7"}

    CPRE = '\033['
    CSUF = '\033[0m'

    ccode = ""
    if attrib:
        for attr in attrib.lower().split():
            attr = attr.strip(",+|")
            if attr in CATTRS:
                ccode += ";" + CATTRS[attr]
    if color in COLORS:
        ccode += ";" + COLORS[color]
    return CPRE + ccode + "m" + text + CSUF

def green(text, attrib=None):
    return colorize(text, "green", attrib)

def red(text, attrib=None):
    return colorize(text, "red", attrib)

def yellow(text, attrib=None):
    return colorize(text, "yellow", attrib)

def blue(text, attrib=None):
    return colorize(text, "blue", attrib)

def purple(text, attrib=None):
    return colorize(text, "purple", attrib)

def cyan(text, attrib=None):
    return colorize(text, "cyan", attrib)

def white(text, attrib=None):
    return colorize(text, "white", attrib)

def black_white(text, attrib=None):
    return colorize(text, "black_white", attrib)

def black_red(text, attrib=None):
    return colorize(text, "black_red", attrib)

def black_green(text, attrib=None):
    return colorize(text, "black_green", attrib)

esc = "\033"
csi = esc + "["
def to(n=1):
    sys.stdout.write(csi + str(n) + "G")
    sys.stdout.flush()

def all_delete():
    sys.stdout.write(csi + "2K")
    sys.stdout.write(csi + "1G")
    sys.stdout.flush()

def n2tail_delete(n):
    to(str(n))
    sys.stdout.write(csi + "0K")
    sys.stdout.write(csi + "1G")
    sys.stdout.flush()

def head2n_delete(n):
    to(str(n))
    sys.stdout.write(csi + "1K")
    sys.stdout.write(csi + "1G")
    sys.stdout.flush()

def down(n=1):
    sys.stdout.write(csi + str(n) + "B")
    sys.stdout.flush()

def up(n=1):
    sys.stdout.write(csi + str(n) + "A")
    sys.stdout.flush()

def overwrite(strings):
    sys.stdout.write("\r")
    sys.stdout.write(strings)

def save():
    sys.stdout.write(csi + "s")
    sys.stdout.flush()

def restore():
    sys.stdout.write(csi + "u")
    sys.stdout.flush()

def lines_delete(n):
    sys.stdout.write(csi + str(n) + "M")

def get_term_size():
    return map(int, os.popen('stty size').read().split())

def clear():
    shell("clear").call()

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
        Usage: dmp(bin binary, split=""/"x"/"d")
    """
    res = binascii.hexlify(binary)
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
    if(value_str[0] == "0"):
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

class screen():
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

class menu():
    def __init__(self, lst, function):
        self.i = 0
        self.lst = lst
        self.num = len(lst)
        self.function = function
        self.top = blue(">", "bold") + "  "
        self.to = 3

    def menu_exit(self):
        restore()
        to(1)
        lines_delete(100)

    def menu_start(self):
        sys.stdout.write(self.top)
        print("")
        for self.i in range(self.num):
            if self.i == 0:
                print(black_red("> ", "bold") + black_white(self.lst[self.i], "bold"))
            else:
                print(black_white(" ") +  " " + self.lst[self.i])
        self.i = 0
        up(self.num+1)
        save()
        to(self.to)
        while 1:
            key = getch()
            restore()
            sys.stdout.write(self.top)
            to(self.to)
            if (key == "j" or ord(key) == DOWN) and self.i < self.num-1:
                down(self.i+1)
                all_delete()
                overwrite(black_white(" ") + " " + self.lst[self.i])
                restore()
                down(self.i+2)
                overwrite(black_red("> ", "bold") + black_white(self.lst[self.i+1], "bold"))
                restore()
                to(3)
                self.i = self.i + 1
            if (key == "k" or ord(key) == UP) and self.i >= 1:
                down(self.i+1)
                all_delete()
                overwrite(black_white(" ") + " " + self.lst[self.i])
                restore()
                down(self.i)
                overwrite(black_red("> ", "bold") + black_white(self.lst[self.i-1], "bold"))
                restore()
                to(3)
                self.i = self.i -1
            elif key == "q" or ord(key) == CTRL_C or ord(key) == CTRL_D:
                self.menu_exit()
                exit()
            elif ord(key) == ENTER:
                self.function(self.i)

