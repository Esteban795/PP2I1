from datetime import datetime as dt
from flask_login import UserMixin

class Client(UserMixin):
    def __init__(self,
                 client_id: int,
                 first_name: str,
                 last_name: str,
                 email: str,
                 password: str,
                 created_at : float = dt.timestamp(dt.now()),
                 recycled_volume : int = 0,
                 is_admin : bool = False):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.recycled_volume = recycled_volume
        self.is_admin = is_admin

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
    
    def get_id(self): #necessary for flask_login
        return self.client_id
