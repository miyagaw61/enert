from .toplevel import *

def mkparser(usage, lst=None):
    """
    usage = '''\
    Usage: git2nd [status] [add] [commit]
    '''
    lst = ['status', 'add', 'commit']
    parser = mkparser(usage, lst)
    args = parser.parse_args(argv[1:])
    ->
    args.command == status or add or commit
    args.args == ['file01', 'file02']
    """
    parser = ArgumentParser(usage=usage, formatter_class=RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    if not lst == None:
        parser.add_argument('command', choices=lst)
    parser.add_argument('args', nargs='*')
    return parser
