
class WasteType:
    def __init__(self,
                 waste_type_id: int,
                 name: str,
                 recyclable:bool):
        self.waste_type_id = waste_type_id
        self.name = name
        self.recyclable = recyclable
        
    def __str__(self):
        return "({0}, recyclable : {1})".format(self.name, self.recyclable)


    def serialize(self):
        '''Méthode de formatage pour ajouter les données dans la DB'''
        return (self.waste_type_id,
                self.name)


