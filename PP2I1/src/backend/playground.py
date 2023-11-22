from datetime import datetime
import Bins
import Client
import Truck
import WasteType
import PickUp
import math

def distance_between_bins(bin1:Bins.Bin, bin2: Bins.Bin) -> float:
    (x1, y1) = bin1.get_position()
    (x2, y2) = bin2.get_position()
    return math.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2)

def distance_between_GPS(point1: (int,int), point2: (int,int)) -> float:
    (x1, y1) = point1
    (x2, y2) = point2
    return math.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2)


def picking_bin_by_truck(bin: Bins.Bin, truck: Truck.Truck) -> Truck.Truck :
    '''Cette fonction enlève les déchets de la Bin passée en paramêtre et l'ajoute dans le Truck passé en paramêtre. \n Elle renvoie le camion. '''

    truck_avail = truck.avail()
    #On retire les déchets présents dans la poubelle
    removed_volume = bin.drain(truck_avail, truck.numberplate)

    #On ajoute les déchets dans le camion
    truck.used += removed_volume

    return truck

def get_amount_of_waste(bins: [Bins.Bin]) -> int:
    '''Cette fonction prend en parametre une liste de Bin et renvoie le total de déchets.'''
    out =  0
    for bin in bins:
        out += bin.used
    return out


def order_bins_by_amount_of_waste(bins: [Bins.Bin]) -> [Bins.Bin]:
    '''Cette focntion prend en parametre une liste de Bin et renvoie cette liste triée en fonction de leur remplissage.'''
    return bins.sort(key=lambda x: x.used)


def order_bins_by_distance(src: (float,float), bins: [Bins.Bin]) -> [Bins.Bin]:
    '''Cette fonction prend en parametre une liste de Bon et renvoie cette lisre triée en fonction de la distance au point de départ src'''
    return bins.sort(key=lambda x:distance_between_GPS(src, x.get_postion()))


def picking_multiple_bins(bins: [Bins.Bin], truck: Truck.Truck) -> Truck.Truck:
    for bin in bins:
        truck = picking_bin_by_truck(bin, truck)
    return truck
