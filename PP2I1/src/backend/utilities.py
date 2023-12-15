from typing import Any
import uuid
from functools import wraps
from flask_login import current_user
from flask import abort
import sqlite3

def checkValidInput(*args : list[Any]):
    """Check if args are both non empty and no only whitespaces"""
    for arg in args:
        if arg == '' or arg.isspace():
            return False
    return True

def generateImgUUID(filename : str):
    """Generate a UUID from a filename"""
    file_ext = filename.split('.')[-1]
    uuid_ = str(uuid.uuid5(uuid.NAMESPACE_DNS, filename))
    return ".".join([uuid_,file_ext])


def admin_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if current_user.is_authenticated and current_user.is_admin == 1:
            return func(*args, **kwargs)
        abort(403)
    return wrapper

def getEuclideanDistance(x1 : tuple[int,int],x2 : tuple[int,int]):
    return ((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2)**0.5

def circularTranslationArray(arr : list[Any],start_index : int):
    return [arr[(start_index + i) % len(arr)] for i in range(len(arr))] 