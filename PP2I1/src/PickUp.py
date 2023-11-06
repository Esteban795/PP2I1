from datetime import datetime as dt


class PickUp:
    def __init__(self, truck_id, bin_id):
        self.truck_id = truck_id
        self.bin_id = bin_id
        self.pickup_time = dt.timestamp(dt.now())


