from datetime import datetime as dt


class PickUp:
    def __init__(self,
                 truck_id: int,
                 bin_id: int):
        self.truck_id = truck_id
        self.bin_id = bin_id
        self.pickup_time = dt.timestamp(dt.now())


    def serialize(self):
        '''Méthode de formatage pour ajouter les données dans la DB'''
        return (self.truck_id,
                self.bin_id,
                self.pickup_time)
