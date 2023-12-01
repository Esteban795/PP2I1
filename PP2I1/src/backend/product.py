class Product:
    def __init__(self,
                 id:int,
                 name: str,
                 price: float,
                 img_url: str,
                 desc: str,
                 volume: int,
                 stock: int):
        self.id = id
        self.name = name
        self.price = price
        self.img_url = img_url
        self.desc = desc
        self.volume = volume
        self.stock = stock


    def serialize(self):
        '''Méthode de formatage pour ajouter les données dans la DB'''
        return (self.id,
                self.name,
                self.price,
                self.img_url,
                self.desc,
                self.volume,
                self.stock)
