class Adventurer():
    def __init__(
            self,
            name,
            rest,
            thirst,
            hunger,
            inventory,
            location,
            escaped=False):
        self.name = name
        self.rest = rest
        self.thirst = thirst
        self.hunger = hunger
        self.inventory = inventory
        self.location = location
        self.escaped = escaped
