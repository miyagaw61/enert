import os, sys, subprocess, re, binascii
from enert import config

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
                "blue": "34", "purple": "35", "cyan": "36", "white": "37"}
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
    """Wrapper for colorize(text, 'cyan')"""
    return colorize(text, "white", attrib)

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
