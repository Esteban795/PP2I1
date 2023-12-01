from typing import Any
import uuid
from functools import wraps
from flask_login import current_user
from flask import abort
import sqlite3


def loadAdminIDs(cur : sqlite3.Cursor) -> set[int]:
    """Load admin IDs from the DB"""
    cur.execute("SELECT client_id FROM clients WHERE is_admin = 1")
    admin_ids = cur.fetchall()
    return {admin_id[0] for admin_id in admin_ids}

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