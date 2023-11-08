from datetime import datetime as dt

class Client:
    def __init__(self,
                 client_id: int,
                 first_name: str,
                 last_name: str,
                 email: str,
                 password: str):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = dt.timestamp(dt.now())
        self.recycled_volume = 0


    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def serialize(self):
        '''Méthode de formatage pour ajouter les données dans la DB'''
        return (self.client_id,
                self.first_name,
                self.last_name,
                self.email,
                self.created_at,
                self.password,
                self.recycled_volume)
