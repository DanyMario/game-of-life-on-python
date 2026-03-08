
class Life:
    def __init__(self,location:tuple,alive:bool):
        self.location = location
        self.alive = alive
        self.neighbors = 0

    def death(self):
        self.alive = False
        self.neighbors = 0

    def set_alive(self):
        self.alive = True
        self.neighbors = 0


    def __repr__(self):
        return f"Life({self.location}, {self.alive})"
