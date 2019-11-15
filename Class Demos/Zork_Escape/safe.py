import item
import room


class Safe(item.Item):
    def __init__(
            self,
            name,
            description,
            helptext,
            openaction,
            location,
            items=[],
            state=False):
        super().__init__(name, description, helptext)
        self.openaction = openaction
        self.location = location
        self.state = state


Cabinet = Safe(
    "Cabinet",
    "A wooden cabinet with a small key hole under the handle",
    "",
    """You use the key in the key hole, the cabinet opens and has a swipe card,
and a Granola Bar, which you take.""",
    room.Kitchen)
FruitBowl = Safe(
    "FruitBowl",
    "A small bowl with what appears to be fruit in it.  Wax Fruit.",
    "",
    """You try to pick up the fruit and it all comes up in one solid wax chunk,
exposing a key... which you take""",
    room.Dining_Room)
Nightstand = Safe(
    "Nightstand",
    "A small nightstand with a card swipe on the side",
    "",
    """You swipe the card in the magenetic reader, the door clicks open and there's
 a paper with '101010' written on it, which you take.""",
    room.Bedroom)
Computer = Safe(
    "Laptop",
    "An older laptop with Windows 10 installed.",
    "",
    """The computer wakes up and begins to print a paper with the number 1000101""",
    room.Living_Room)
FrontDoor = Safe(
    "Door",
    "A large thick wooden door with a lit up keypad next to it.",
    "",
    "The door creaks open...",
    room.Foyer)
