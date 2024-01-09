from typing import Any
import requests
import urllib.parse
import uuid
from functools import wraps
from flask_login import current_user
from flask import abort
import math

def checkValidInput(*args : list[Any]):
    """Check if args are both non empty and no only whitespaces"""
    for arg in args:
        if arg == '' or arg.isspace():
            return False
    return True


def runLengthEncoding(lst : list[int]):
    d = dict.fromkeys(lst, 0)
    for i in lst:
        d[i] += 1
    return d

def runLengthDecoding(d : dict[int,int]):
    lst = []
    for i in d:
        for j in range(d[i]):
            lst.append(i)
    return lst

def getLatLongFromStreetAdress(address : str):
    url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(address) +'&format=json'
    response = requests.get(url).json()
    return response[0]["lat"],response[0]["lon"]

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

def getHaversineDistance(x1 : tuple[float,float],x2 : tuple[float,float]):
    """Return the distance between two points on Earth using the Haversine formula"""
    R = 6371.0710 # Radius of the Earth in km
    lat1,lon1 = x1
    lat2,lon2 = x2
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (dlat/2)**2 + (dlon/2)**2 * math.cos(lat1) * math.cos(lat2)
    return 2 * R * math.asin(a**0.5)