
class Truck:
    def __init__(self,
                 truck_id: int,
                 numberplate: str,
                 capacity: int):
        self.truck_id = truck_id
        self.numberplate = numberplate
        self.capacity = capacity
        self.used = 0

    def avail(self) -> int:
        '''La méthode avail renvoie la place disponible dans l'objet Truck.'''
        return self.capacity - self.used

    def add_waste(self, volume: int) -> None:
        '''La méthode add_waste permet d'ajouter des déchets dans l'objet Truck. Elle prend en parametre un
         entier qui représente le volume de déchets à ajouter. '''
        if volume < 0:
            raise ValueError('negative volume')
        if volume > self.avail():
            raise ValueError('overflow volume')
        self.used += volume

    def fill(self, volume: int) -> int:
        '''La méthode fill prend en paramêtre un volume et remplie au maximum l'objet Truck.
        Elle renvoie le volume ajouté à l'objet Truck'''
        if volume < 0:
            raise ValueError('negative volume')
        c = min(self.avail(), volume)
        self.used += c
        return c

    def empty(self) -> int:
        ''' La méthode empty vide l'objet camion et renvoie le volume qui vient d'être vidé.'''
        c = self.used
        self.used -= c
        return c


    def __str__(self):
        return "Camion : {0}, ({1}/{2})".format(self.numberplate, self.used, self.capacity)


    def serialize(self):
        '''Méthode de formatage pour ajouter les données dans la DB'''
        return (self.truck_id,
                self.numberplate,
                self.used,
                self.capacity)


