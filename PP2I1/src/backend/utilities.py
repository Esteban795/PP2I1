from typing import Any
from collections import OrderedDict

def checkValidInput(*args : list[Any]):
    """Check if args are both non empty and no only whitespaces"""
    for arg in args:
        if arg == '' or arg.isspace():
            return False
    return True


def runLengthEncoding(lst : list[int]):
    d = OrderedDict.fromkeys(lst, 0)
    for i in lst:
        d[i] += 1
    return [(k, v) for k, v in d.items()]