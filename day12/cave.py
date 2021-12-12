class Cave:

    def __init__(self, name):
        self.links = []
        self.name = name
        self.is_small = name.islower()
    
    def add_link(self, cave):
        self.links.append(cave)
    
    def __eq__(self, other):
        return self.name == other.name