class Room():
    def __init__(
            self,
            name,
            description,
            helptext,
            items=[],
            validdirection={}):
        self.name = name
        self.description = description
        self.helptext = helptext
        self.items = items
        self.validdirection = validdirection


Dining_Room = Room(
    "Dining Room",
    """You see a cabinet in the corner and a bowl of fruit on a table.
There is a door to the West and North""",
    "You can open the cabinet and look in the fruit bowl")

Foyer = Room("Foyer",
             """You see a big wooden front door with a keypad on
the wall next to it. There are doors leading to the North,
East, and West""",
             "You can try to unlock the door... if you know the code")

Kitchen = Room("Kitchen",
               """You see a cabinet, a counter with a sink, and a drawer.
The drawer seems jammed.  The only exit is to the South""",
               "You can open the cabinet if you have a key.")

Living_Room = Room(
    "Living Room",
    """You see a well worn lounge chair and a locked laptop in front
of an old broken tv.  You can only go East from here.""",
    "You can try to unlock the laptop if you have a PIN.")

Bedroom = Room("Bedroom",
               """You see a dirty unmade bed with a lockable nightstand next
to it with a card reader on it. There is a door to the
West and to the South.""",
               "You can open the nightstand if you have a keycard.")

Bathroom = Room("Bathroom",
                """You can see a dirty bathtub, a dirty sink, and an unsanitary
commode.  You can go East from here.""",
                "Not much to see here....")
