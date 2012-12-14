# -*- coding: utf-8 -*-
import json
def print_exception_message(*args):
    """ 例外を補足し、例外メッセージを表示するデコレーター
    """
    def wrapper(func):
        exceptions = tuple(item for item in args if issubclass(item, Exception)) or (Exception,)
        def newfunc(*args, **kwargs):
            try:
                func(*args, **kwargs)

            except exceptions, e:
                try:
                    errors = json.loads(e.reason.replace("'", '"'))
                except:
                    errors = [dict(message=e.reason)]

                for error in errors:
                    print "{classname}: {message}".format(
                            classname = e.__class__.__name__,
                            message = error.get('message'), 
                            )

                print
        return newfunc
    return wrapper
