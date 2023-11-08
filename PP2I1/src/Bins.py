from datetime import datetime as dt

class Bin:
    def __init__(self,
                 bin_id: int,
                 owner_id:int,
                 lat: float,
                 long:float,
                 capacity: int,
                 waste_type:int,
                 last_emptied=None,
                 last_emptied_by=None):
        self.bin_id = bin_id
        self.onwer_id = owner_id
        self.lat = lat
        self.long = long
        self.capacity = capacity
        self.used = 0
        self.created = dt.timestamp(dt.now())
        self.last_emptied = last_emptied
        self.last_emptied_by = last_emptied_by
        self.waste_type = waste_type


    def avail(self) -> int:
        '''La méthode avail renvoie le volume disponible dans l'objet Bin'''
        return self.capacity - self.used

    def used_percentage(self) -> float:
        '''La méthode used_percentage renvoie le pourcentage occupé dans l'objet Bin'''
        if self.capacity == 0:
            raise ValueError('capacity is nul')
        return self.used / self.capacity * 100

    def add_waste(self, volume: int) -> None:
        '''La méthode add_waste ajoute, si possible, le volume passé en paramètre dans l'objet Bin'''
        if volume < 0:
            raise ValueError('negative volume')
        if volume > self.avail() :
            raise ValueError('to much waste to add ')
        self.used += volume

    def fill(self, volume: int) -> int:
        '''La méthode fill prend en paramêtre un volume et remplit au maximum l'objet Bin.
        Elle renvoie le volume ajouté à l'objet Bin '''
        if volume < 0:
            raise ValueError('negative volume')
        c = min(volume, self.avail())
        self.used += c
        return c

    def drain(self, volume: int, truck_id) -> int:
        '''La méthode drain prend en parametre un volume, et vide la poubelle de ce volume ou jusqu'à
        ce que la poubelle soit vide ou le volume soit vide. Elle renvoie le volume qui à été vidé de la poubelle. '''
        if volume < 0:
            raise ValueError('negative volume')
        c = min(volume, self.used)
        self.used -= c
        self.last_emptied_by = truck_id
        return c

    def get_position(self):
        '''La méthodé get_position renvoie les coordonnée GPS de l'objet Bin'''
        return (self.lat, self.long)

    def __str__(self):
        return "Poubelle : {0}, ({1}/{2})".format(self.owner_id, self.used, self.capacity)

    def serialize(self):
        '''Méthode de formatage pour ajouter les données dans la DB'''
        return (self.bin_id,
                self.owner_id,
                self.lat,
                self.long,
                self.used,
                self.capacity,
                self.last_emptied,
                self.last_emptied_by,
                self.created,
                self.waste_type)



