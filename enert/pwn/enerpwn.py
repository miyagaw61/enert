from enert.init import *
from .toplevel import *

def p(n, bit):
    return make_packer(bit)(n)

def u(x, bit):
    return make_unpacker(bit)(x)

def allp(n):
    return make_packer('all')(n)

def allu(x):
    if arch == 64:
        return make_unpacker(len(x)*8)(x)
    else:
        return make_unpacker(len(x)*4)(x)
