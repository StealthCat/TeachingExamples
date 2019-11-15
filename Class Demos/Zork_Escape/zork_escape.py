import sys
import adventurer
import item
import consumable
import usable
import safe
import room


def show_inventory(player):
    if not player.inventory:
        print("Your bag is empty.")
    else:
        print("You have: ")
        for invlist in player.inventory:
            print(f"{invlist}")
    player.hunger += 1
    player.thirst += 1


def show_health(player):
    print(
        f"Energy: {player.rest}, Hunger: {player.hunger}, Thirst: {player.thirst}")


def movement(player, cmd):
    if cmd in (player.location.validdirection):
        player.location = player.location.validdirection[cmd]
        print(
            f"You are now in {player.location.name}, {player.location.description}")
    else:
        print("You can't go that way, please choose from: ", end="")
        for key in player.location.validdirection.keys():
            print(f"{key} ", sep=" ", end="")
        print("\n")
    player.hunger += 1
    player.thirst += 1
    player.rest -= 1


def look_room(player):
    print(f"{player.location.name}: {player.location.description}")
    print(f"Hint: {player.location.helptext}\n")
    for stuff in player.location.items:
        print("You see ", end="")
        print(f"{stuff.name}", sep=" ", end="")
        print(f" in the {player.location.name}.")
    player.hunger += 1
    player.thirst += 1


def open_item(player):
    if player.location.name == "Dining Room":
        if not player.location.items[0].state:
            print(safe.FruitBowl.openaction)
            player.inventory.update({usable.Key.name: usable.Key})
            player.location.items[0].state = True
        else:
            print("The bowl is empty.")
    elif player.location.name == "Kitchen":
        if not player.location.items[0].state:
            if 'Key' in player.inventory:
                print(safe.Cabinet.openaction)
                player.inventory.update({usable.Card.name: usable.Card})
                player.inventory.update(
                    {consumable.SnackBar.name: consumable.SnackBar})
                player.location.items[0].state = True
            else:
                print("You need a key to open this.")
        else:
            print("The Cabinet is already open and empty.")
    elif player.location.name == "Bedroom":
        if not player.location.items[0].state:
            if 'Card' in player.inventory:
                print(safe.Nightstand.openaction)
                player.inventory.update(
                    {usable.PassPaper.name: usable.PassPaper})
                player.location.items[0].state = True
            else:
                print("You need a magnetic swipe card to open this.")
        else:
            print("The Nightstand is already open and empty.")
    elif player.location.name == "Living Room":
        if not player.location.items[0].state:
            if 'Paper' in player.inventory:
                print(safe.Computer.openaction)
                player.inventory.update(
                    {usable.DoorCode.name: usable.DoorCode})
                player.location.items[0].state = True
            else:
                print("You need a PIN to access the login.")
        else:
            print("The computer is of no more use to you.")
    elif player.location.name == "Foyer":
        if not player.location.items[0].state:
            if 'Code' in player.inventory:
                print(safe.FrontDoor.openaction)
                player.location.items[0].state = True
                player.escaped = True
            else:
                print(
                    f"""Come on, {player.name}, you didn't think it would be this easy...
                did you?""")
    else:
        print("Nothing in here to open.")


def look_item(player):
    for stuff in player.location.items:
        print(f"You see {stuff.name}, {stuff.description}")
    player.hunger += 1
    player.thirst += 1


def use_item(player):
    if 'Granola' in player.inventory:
        if consumable.SnackBar.state:
            chooseeat = input(
                f"""\nDo you want to eat your snacks now, {player.name}?
You are {player.hunger}% hungry. (Y/N)""")
            if str.upper(chooseeat) == "Y":
                consumable.SnackBar.state = False
                player.hunger = 0
                print("Yummy!  You are 0 % hungry\n")
            else:
                print("Good idea, save it for  when you really need it.\n")
        else:
            print("You already ate your snack bar.")
    if 'Bottle' in player.inventory:
        if consumable.WaterBottle.state:
            choosedrink = input(
                f"""\nDo you want to drink you water now, {player.name}?
You are {player.thirst}% thirsty. (Y/N) """)
            if str.upper(choosedrink) == "Y":
                consumable.WaterBottle.state = False
                player.thirst = 0
                print("Hydrate!  You are 0 % thirsty.\n")
            else:
                print("Good idea, save it for  when you really need it.\n")
        else:
            print("You've already drank your water.")
    else:
        print(f"You don't nave anything I can use.")


def take_item(player):
    if len(player.location.items) > 0:
        try:
            tempdict = {}
            k = 1
            for v in player.location.items:
                tempdict.update({k: v})
                print(f"{k}: {v.name}")
                k += 1
            invitem = input("What item number you like to take? ")
            invdict = tempdict[int(invitem)]
            if invdict.name in ('Cabinet', 'Nightstand', 'Computer', 'Door'):
                print("\nYou can't take that.")
            elif invdict.name == ('FruitBowl'):
                print(
                    "\nWhy would you want wax fruit... ew?  Maybe there's something inside.")
            else:
                player.inventory.update({invdict.name: invdict})
                player.location.items.pop(int(invitem) - 1)
                print(f"You took {invdict.name}")
        except KeyError:
            print("Invalid selection, try again.")
    else:
        print("There are no items to take.")
    player.hunger += 1
    player.thirst += 1


def quit_game(player):
    print(f"""Suicide, eh?  Just couldn't take it any more?
Zeroing your energy level, and.....

    You died.
    Energy: 0, Hunger: {player.hunger}, Thirst: {player.thirst}

    """)
    sys.exit()


def show_menu():
    menu = """
          Inventory........... I or i | Health.............. H or h
          Move North.......... N or n | Move East........... E or e
          Move South.......... S or s | Move West........... W or w
          Take Item........... T or t | Use (eat|drink)..... U or u
          Look at items....... L or l | Look around Room.....R or r
          Open Item............O or o | Quit................ Q or q
        """
    print(menu)


def show_loc(room):
    print(f"\nYou're in the {room.name}: {room.description}")


def main():
    choosename = input("\n\nWould you like to create your name? (Y/N) ")
    name = "Meatbag"
    if str.upper(choosename) == "Y":
        name = input("What is your name? ")

    player = adventurer.Adventurer(name, 100, 0, 0, {}, room.Foyer)

    print("\n\nWelcome to Zork Escape!")
    print("You've entered a room and the door slammed behind you.")
    print("It's up to you to figure out how to get out.")
    print(f"Check your health, watch your stats.  Good luck, {player.name}!")
    show_loc(player.location)

    room.Kitchen.validdirection = {"S": room.Dining_Room}
    room.Dining_Room.validdirection = {"W": room.Foyer,
                                       "N": room.Kitchen}
    room.Foyer.validdirection = {"W": room.Living_Room,
                                 "N": room.Bedroom,
                                 "E": room.Dining_Room}
    room.Bathroom.validdirection = {"E": room.Bedroom}
    room.Bedroom.validdirection = {"S": room.Foyer,
                                   "W": room.Bathroom}
    room.Living_Room.validdirection = {"E": room.Foyer}

    room.Kitchen.items = [safe.Cabinet]
    room.Dining_Room.items = [safe.FruitBowl]
    room.Foyer.items = [safe.FrontDoor, item.DoorStop, item.WoodBlock]
    room.Bathroom.items = [item.ToiletBrush, consumable.WaterBottle]
    room.Bedroom.items = [safe.Nightstand]
    room.Living_Room.items = [safe.Computer]

    safe.FruitBowl.contains = [usable.Key]
    safe.Cabinet.contains = [consumable.SnackBar, usable.Card]
    safe.Nightstand.contains = [usable.PassPaper]

    menu_items = {
        'I': show_inventory,
        'H': show_health,
        'R': look_room,
        'L': look_item,
        'U': use_item,
        'T': take_item,
        "O": open_item,
        'N': movement,
        'S': movement,
        'E': movement,
        'W': movement,
        'Q': quit_game}

    while (player.escaped == False
           and player.rest > 0
           and player.hunger < 101
           and player.thirst < 101):

        show_menu()
        cmd = str.upper(input("Enter Command: ")[:1])
        print()
        if cmd == 'Q':
            quit_game(player)

        func = menu_items.get(cmd)
        if func is None:
            print("Invalid Command!!", file=sys.stderr)
            continue
        elif cmd in ("H", "I", "L", "T", "R", "U", "O"):
            func(player)
        elif cmd in ("N", "S", "E", "W"):
            func(player, cmd)
        else:
            func()

    if player.escaped:
        print(f"\nCongratulations, {name}, you made it!")
        print(f"Energy: {player.rest}, Hunger: {100 - player.hunger}, Thirst: {100 - player.thirst} remaining.\n")
    elif player.rest == 0:
        print("\n\nToo many moves used, try again!")
        print(f"Energy: {player.rest}, Hunger: {player.hunger}, Thirst: {player.thirst}")
    elif player.hunger >= 100:
        print("\n\nSnickers satisfies... you should try one some time.  You died of Hunger.")
        print(f"Energy: {player.rest}, Hunger: {player.hunger}, Thirst: {player.thirst}")
    else:
        print("\n\nYou should really look into r/HydroHomies.  You died of Thirst.")
        print(f"Energy: {player.rest}, Hunger: {player.hunger}, Thirst: {player.thirst}")


if __name__ == "__main__":
    main()
