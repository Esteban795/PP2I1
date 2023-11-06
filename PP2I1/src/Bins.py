from datetime import datetime as dt

class Bins:
    def __init__(self,
                 onwer_id,
                 lat,
                 long,
                 capacity,
                 waste_type,
                 last_emptied=None,
                 last_emptied_by=None):
        self.onwer_id = onwer_id
        self.lat = lat
        self.long = long
        self.capacity = capacity
        self.used = 0
        self.created  = dt.timestamp(dt.now())
        self.last_emptied = last_emptied
        self.last_emptied_by = last_emptied_by
        self.waste_type = waste_type


    def avail(self):
        return self.capacity - self.used

    def used_percentage(self):
        if self.capacity == 0:
            raise ValueError('capacity is nul')
        return self.used / self.capacity * 100

    def add_waste(self, volume):
        if volume < 0:
            raise ValueError('negative volume')
        if volume > self.avail() :
            raise ValueError('to much waste to add ')

        self.used += volume

    def fill(self, volume):
        if volume < 0:
            raise ValueError('negative volume')
        c = min(volume, self.avail())
        self.used += c
        return c

    def drain(self, volume, truck_id):
        if volume < 0:
            raise ValueError('negative volume')
        c = min(volume, self.used)
        self.used -= c
        self.last_emptied_by = truck_id
        return c

    def get_position(self):
        return (self.lat, self.long)

    def __str__(self):
        return "Poubelle : {0}, ({1}/{2})".format(self.onwer_id, self.used, self.capacity)
