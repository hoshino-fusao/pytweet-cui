# -*- coding: utf-8 -*-
def parseargs(args, default_key=None):
    """ 入力した引数をパースし、dictで返す
    
    引数をパースできなかった時は、空の dict を返すが、
    default_key を指定しておけばそれを key として args をまるっと格納する。

    Cmd(cmd.py)の引数について:
    Cmdでは引数をパースしてくれないため、引数を複数した使い方ができない。
    """
    dict_args = dict()
    try:
        if args:
            dict_args = dict(tuple(arg.split('=')) for arg in args.split())
    except:
        if default_key:
            dict_args = {default_key: args}

    return dict_args
