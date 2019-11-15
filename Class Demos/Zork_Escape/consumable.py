import item


class Consumable(item.Item):
    def __init__(self,
                 name,
                 description,
                 helptext,
                 state=True):
        super().__init__(name, description, helptext)
        self.state = state


WaterBottle = Consumable(
    "Bottle",
    "A bottle... with water in it",
    "Water!  It's what plants crave!")
SnackBar = Consumable(
    "Granola",
    "May contain nuts, fruits, gluten, and sugar... and cardboard",
    "You're not the same when you're hungry...")
