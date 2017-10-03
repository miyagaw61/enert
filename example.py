from collections import OrderedDict
import better_exceptions
from enert import *

d = enerdict(zero="0", one="1", two="2", three="3")

msg = """\
d = enerdict(zero="0", one="1", two="2", three="3")\
"""

inf(msg, "declare: \n")
inf(type(d), "type: ")
inf(d, "core: ")
inf(d.key(0), "d.key(0): ")
inf(d.value(1), "d.value(1): ")
inf(d.list, "d.list: ")
inf(d.keys, "d.keys: ")
inf(d.values, "d.values: ")

d.append("four", "4")
inf(d.list, "d.list: ")
inf(d.keys, "d.keys: ")
inf(d.values, "d.values: ")

#msg = """\
#for key in d:
#    print(key)\
#"""
#inf(msg, "")
#for key in d:
#    print(key)
#
#msg = """\
#for key,value in d.list:
#    print("key is " + key + ", value is " + value)\
#"""
#inf(msg, "")
#for key,value in d.list():
#    print("key is " + key + ", value is " + value)\
