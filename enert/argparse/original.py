from .toplevel import *

def mkparser(usage, lst):
    parser = ArgumentParser(usage=usage, formatter_class=RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('others', nargs='*')
    parser.add_argument('command', choices=lst)
    return parser
