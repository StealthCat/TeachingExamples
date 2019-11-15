class Item():
    def __init__(self,
                 name,
                 description,
                 helptext):
        self.name = name
        self.description = description
        self.helptext = helptext


WoodBlock = Item(
    "Block",
    "Wood... in block form.",
    "You could use this for something probably?")
DoorStop = Item(
    "Doorstop",
    "A rubber door stop to hold doors open.",
    "This would have been helpful right before the game started.")
ToiletBrush = Item(
    "Brush",
    "Toilet Brush, white handle, mostly white bristles with flecks of toilet paper and... not toilet paper",
    "The thing you clean toilets with")
