import item


class Usable(item.Item):
    def __init__(self,
                 name,
                 description,
                 helptext,
                 use=None):
        super().__init__(name, description, helptext)
        self.use = use


Key = Usable(
    "Key",
    "A small brass key",
    "You can probably unlock something with it...")
Card = Usable(
    "Card",
    "A blue card with a magnetic strip on the back",
    "I wouldn't put it in an ATM...")
PassPaper = Usable(
    "Paper",
    "It has 101010 written on it.",
    "Maybe it's a Personal PIN Number to use in an Automated ATM Machine?")
DoorCode = Usable(
    "Code",
    "A paper with the number 1000101 written on it.",
    "Binary... heh.")
