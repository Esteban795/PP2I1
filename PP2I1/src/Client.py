from datetime import datetime as dt

class Client:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created = dt.timestamp(dt.now())
        self.recycled_volume = 0


    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)
