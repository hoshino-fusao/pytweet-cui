# -*- coding: utf-8 -*-

def parseargs(args):
    """ 入力した引数をパースし、dictで返す
    
    Cmd(cmd.py)の引数について:
    Cmdでは引数をパースしてくれないため、引数を複数した使い方ができない。
    """
    dict_args = dict()
    try:
        if args:
            dict_args = dict(tuple(arg.split('=')) for arg in args.split())
        return dict_args

    except:
        return None


