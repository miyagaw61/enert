from .toplevel import *

def mkparser(usage):
    """
    parser = mkparser(usage)
    parser.add_argument('command', choices=lst)
    parser.add_argument('args', nargs='*')
    args = parser.parse_args(argv[1:)
    """
    parser = ArgumentParser(usage=usage, formatter_class=RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    return parser
