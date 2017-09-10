import os, sys, subprocess, re, binascii, fcntl, termios

class file:
    def __init__(self, file_name):
        self.name = file_name

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
        return [stdout_str.decode(), stderr_str.decode()]

    def call(self):
        cmd = self.cmd.split()
        subprocess.call(cmd)

def colorize(text, color=None, attrib=None):
    """
    Colorize text using ansicolor
    ref: https://github.com/hellman/libcolors/blob/master/libcolors.py
    """
    # ansicolor definitions
    COLORS = {"black": "30", "red": "31", "green": "32", "yellow": "33",
            "blue": "34", "purple": "35", "cyan": "36", "white": "37", 
            "black_white": "40;37", "black_red": "40;31"}
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
    """Wrapper for colorize(text, 'green')"""
    return colorize(text, "green", attrib)

def red(text, attrib=None):
    """Wrapper for colorize(text, 'red')"""
    return colorize(text, "red", attrib)

def yellow(text, attrib=None):
    """Wrapper for colorize(text, 'yellow')"""
    return colorize(text, "yellow", attrib)

def blue(text, attrib=None):
    """Wrapper for colorize(text, 'blue')"""
    return colorize(text, "blue", attrib)

def purple(text, attrib=None):
    """Wrapper for colorize(text, 'purple')"""
    return colorize(text, "purple", attrib)

def cyan(text, attrib=None):
    """Wrapper for colorize(text, 'cyan')"""
    return colorize(text, "cyan", attrib)

def white(text, attrib=None):
    """Wrapper for colorize(text, 'white')"""
    return colorize(text, "white", attrib)

def black_white(text, attrib=None):
    """Wrapper for colorize(text, 'black_white')"""
    return colorize(text, "black_white", attrib)

def black_red(text, attrib=None):
    """Wrapper for colorize(text, 'black_red')"""
    return colorize(text, "black_red", attrib)

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

class menu():
    def __init__(self, lst, function):
        self.i = 0
        self.lst = lst
        self.num = len(lst)
        self.function = function
        self.top = blue(">", "bold") + "  "
        self.to = 3
        self.ENTER = 13
        self.CTRL_C = 3
        self.CTRL_D = 4
        self.UP = 65
        self.DOWN = 66

    def menu_exit(self):
        restore()
        to(1)
        sys.stdout.write(csi + str(self.num) + "M")
        all_delete()

    def menu_start(self):
        save()
        sys.stdout.write(self.top)
        print("")
        for self.i in range(self.num):
            if self.i == 0:
                print(black_red("> ", "bold") + black_white(self.lst[self.i], "bold"))
            else:
                print("  " + self.lst[self.i])
        self.i = 0
        restore()
        to(self.to)
        while 1:
            key = getch()
            restore()
            sys.stdout.write(self.top)
            to(self.to)
            if (key == "j" or ord(key) == self.DOWN) and self.i < self.num-1:
                down(self.i+1)
                all_delete()
                overwrite("  " + self.lst[self.i])
                restore()
                down(self.i+2)
                overwrite(black_red("> ", "bold") + black_white(self.lst[self.i+1], "bold"))
                restore()
                to(3)
                self.i = self.i + 1
            if (key == "k" or ord(key) == self.UP) and self.i >= 1:
                down(self.i+1)
                all_delete()
                overwrite("  " + self.lst[self.i])
                restore()
                down(self.i)
                overwrite(black_red("> ", "bold") + black_white(self.lst[self.i-1], "bold"))
                restore()
                to(3)
                self.i = self.i -1
            elif key == "q" or ord(key) == self.CTRL_C or ord(key) == self.CTRL_D:
                self.menu_exit()
                exit()
            elif ord(key) == self.ENTER:
                self.function(self.i)
