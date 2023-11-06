
class Truck:
    def __init__(self, numberplate, capacity):
        self.numberplate = numberplate
        self.capacity = capacity
        self.used = 0

    def avail(self):
        return self.capacity - self.used

    def add_waste(self, volume):
        if volume < 0:
            raise ValueError('negative volume')
        if volume > self.avail():
            raise ValueError('overflow volume')


    def fill(self,volume):
        if volume < 0:
            raise ValueError('negative volume')
        c = min(self.avail(), volume)
        self.used += c
        return c

    def empty(self):
        c = self.used
        self.used -= c
        return c


    def __str__(self):
        return "Camion : {0}, ({1}/{2})".format(self.numberplate, self.used, self.capacity)




