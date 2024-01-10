from typing import Any
import requests
import urllib.parse

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