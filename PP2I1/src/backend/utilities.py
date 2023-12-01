from typing import Any
import uuid

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