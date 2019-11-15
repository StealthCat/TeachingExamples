import random
from statistics import mean
from os import getcwd
import time

###########################################
#           Character Generator           #
###########################################


class playerCharacter(object):

    players = {}

    def __init__(self, name="", race="",
                 stat_list={"Strength": 0, "Dexterity": 0,
                            "Constitution": 0, "Intelligence": 0,
                            "Wisdom": 0, "Charisma": 0},
                 char_class="", race_source=""):
        self.name = name
        self.stat_list = stat_list
        self.race = race
        self.char_class = char_class
        self.race_source = race_source
        playerCharacter.players[self.name] = self

    def __repr__(self):
        return "{0.name}: {0.race} {0.char_class} -- Stats: {0.stat_list}\n" \
               "For more info on {0.race}, see {0.race_source}.\n".format(self)


def race_and_stats():
    with open(r"names\player_races.txt", 'r') as race_file:
        race_list = race_file.readlines()
    raw_player_race = random.choice(race_list).split(",")
    player_race = raw_player_race[0]
    stat_list = raw_player_race[1:-1]
    race_source = raw_player_race[-1]
    player_dict = {}
    player_dict.update({"race": player_race})
    stats_dict = {}
    for i in range(len(stat_list)):
        stats_dict.update({stat_list[i][0:-3].strip(): int(stat_list[i][-1])})
    if player_race == "Half-Elf":
        increased_stats = 0
        while increased_stats <= 2:
            random_stat = random.choice(["Strength", "Dexterity",
                                         "Constitution", "Intelligence",
                                         "Wisdom"])
            if stats_dict[random_stat] == 0:
                stats_dict[random_stat] += 1
                increased_stats += 1
        else:
            pass
    player_dict.update({"stat_list": stats_dict,
                        "race_source": race_source.strip()})
    return(player_dict)


def stat_generator(stat_list):
    for i in range(6):
        dice_rolls = [random.randint(1, 6), random.randint(1, 6),
                      random.randint(1, 6), random.randint(1, 6)]
        low_roll = min(dice_rolls)
        dice_rolls.remove(low_roll)
        stat_num = sum(dice_rolls)
        if i == 0:
            stat_list["Strength"] += stat_num
        if i == 1:
            stat_list["Dexterity"] += stat_num
        if i == 2:
            stat_list["Constitution"] += stat_num
        if i == 3:
            stat_list["Intelligence"] += stat_num
        if i == 4:
            stat_list["Wisdom"] += stat_num
        if i == 5:
            stat_list["Charisma"] += stat_num
    return(stat_list)


def get_name(new_character):
    player_race = new_character["race"].split(" ")[-1]
    with open("names\\"+player_race.lower()+"_names.txt", 'r') as names_f:
        name_list = names_f.readlines()
    character_name = ""
    while character_name == "":
        character_name = random.choice(name_list).strip()
        if character_name in playerCharacter.players:
            character_name = ""
    return character_name


def assign_class(new_character):
    reversed_stats = [(value, key) for key, value in
                      new_character["stat_list"].items()]
    sorted_stats = sorted(reversed_stats, reverse=True)
    top_stat = sorted_stats[0][1]
    second_stat = sorted_stats[1][1]
    if top_stat == "Constitution":
        return "Barbarian"
    if top_stat == "Intelligence":
        return "Wizard"
    if top_stat == "Strength":
        return "Fighter"
    if top_stat == "Dexterity":
        if second_stat == "Wisdom":
            return "Ranger"
        else:
            return "Rogue"
    if top_stat == "Wisdom":
        if second_stat == "Strength" or second_stat == "Constitution":
            return "Cleric"
        elif second_stat == "Dexterity":
            return "Monk"
        else:
            return "Druid"
    if top_stat == "Charisma":
        if second_stat == "Dexterity":
            return "Bard"
        elif second_stat == "Intelligence":
            return "Sorcerer"
        elif second_stat == "Wisdom":
            return "Warlock"
        else:
            return "Paladin"


def char_generator():
    num_to_gen = 0
    while num_to_gen < 1 or num_to_gen > 10:
        try:
            num_to_gen = int(input("How many characters would you like to "
                                   "generate? "))
            if num_to_gen > 10:
                print("This generator only creates up to 10 characters at a "
                      "time")
                pass
            if num_to_gen < 1:
                print("Please enter a positive number.")
                pass
        except (ValueError, TypeError):
            print("Please enter a number.")
            pass
    for i in range(num_to_gen):
        new_pc = race_and_stats()
        new_pc.update({"stat_list": stat_generator(new_pc["stat_list"])})
        new_pc.update({"name": get_name(new_pc)})
        new_pc.update({"char_class": assign_class(new_pc)})
        new_pc = playerCharacter(new_pc["name"], new_pc["race"],
                                 new_pc["stat_list"], new_pc["char_class"],
                                 new_pc["race_source"])
    print("\n")
    with open("generated_characters.txt", mode='a') as output_file:
        for i in playerCharacter.players:
            print(playerCharacter.players[i])
            output_file.write(str(playerCharacter.players[i]))
    print(r"Your characters have been saved in {}\generated_characters.txt."
          .format(getcwd()))


###########################################
#           Encounter Generator           #
###########################################

def encounter_level_generator():
    levels = []
    group_size = 0
    while group_size < 4 or group_size > 6:
        try:
            group_size = int(input("How many players are in the group? "))
            if group_size > 6 or group_size < 4:
                print("This generator cannot create encounters for fewer "
                      "than 4 or more than 6 players")
                pass
        except (ValueError, TypeError):
            print("There must be a positive number of players. "
                  "Please enter a number.")
            pass
    while len(levels) < group_size:
        temp_lvl = input("What is the level of player #{}: "
                         .format(len(levels)+1))
        try:
            if int(temp_lvl) > 0 and int(temp_lvl) <= 20:
                levels.append(int(temp_lvl))
            else:
                raise ValueError
        except ValueError:
            print("Player level must be a number between 1 and 20.")
    if max(levels) - min(levels) > 3:
        print("")
        print("Warning: There is more than a 3 level difference between the "
              "lowest and highest level characters.")
        print("Encounter may not be balanced.\n")
    if max(levels) == 20:
        print("")
        print("Warning: Level 20 characters can vary wildly in power level. ")
        print("Encounter may not be balanced.\n")
    return levels


def get_solo_encounter(levels):
    cr_solo = 0
    avg_level = int(mean(levels))
    final_solo = []
    with open(r"monsters\level_to_solo_cr.txt", 'r') as cr_solo_file:
        cr_solo_list = cr_solo_file.readlines()
    for i in cr_solo_list:
        final_solo.append(i.strip().split(","))
    for i in final_solo:
        if int(i[0]) == avg_level:
            cr_solo = i[len(levels)-3]
        else:
            pass
    monster_list = []
    with open(r"monsters\monsters.txt", 'r') as monster_file:
        monster_list_raw = monster_file.readlines()
    for i in monster_list_raw:
        monster_list.append(i.strip().split(","))
    monster_choices = []
    for i in range(len(monster_list)):
        if monster_list[i][-3] == cr_solo:
            monster_choices.append(monster_list[i])
        else:
            pass
    encounter_monster = random.choice(monster_choices)
    localtime = time.localtime(time.time())
    f_name = "generated_monsters_" + str(localtime[0]) + str(localtime[7]) \
                                   + str(localtime[3]) + str(localtime[4]) \
                                   + str(localtime[5]) + ".txt"
    with open("generated_encounters\\"+f_name, mode='w') as mon_export:
        mon_export.write("The following list of monsters has been"
                         "randomly generated: \n")
        mon_export.write("The selected encounter is a {}. please see {} for "
                         "more information."
                         .format(encounter_monster[0], encounter_monster[-1]))

    print("")
    print("The selected encounter is a {}. please see {} for more information."
          .format(encounter_monster[0], encounter_monster[-1]))
    print()
    print(r"The encounter has been saved in {}\generated_encounters\{}"
          .format(getcwd(), f_name))


def get_double_encounter(levels):
    cr_double = []
    final_double = []
    double_monster_list = []
    cr_list = []
    with open(r"monsters\level_to_double_cr.txt", 'r') as cr_double_file:
        cr_double_list = cr_double_file.readlines()
    for i in cr_double_list:
        final_double.append(i.strip().split(","))
    for i in levels:
        for i2 in final_double:
            if i2[0] == str(i):
                cr_double.append(i2[1:])
    for i in range(len(cr_double)):
        for i2 in range(len(cr_double[i])):
            cr_list.append(cr_double[i][i2])
    monster_list = []
    with open(r"monsters\monsters.txt", 'r') as monster_file:
        monster_list_raw = monster_file.readlines()
    for i in monster_list_raw:
        monster_list.append(i.strip().split(","))
    for i in range(len(cr_list)):
        monster_choices = []
        for mon_i in range(len(monster_list)):
            if monster_list[mon_i][-3] == cr_list[i]:
                monster_choices.append(monster_list[mon_i])
        double_monster_list.append(random.choice(monster_choices))
    localtime = time.localtime(time.time())
    f_name = "generated_monsters_" + str(localtime[0]) + str(localtime[7]) \
                                   + str(localtime[3]) + str(localtime[4]) \
                                   + str(localtime[5]) + ".txt"
    with open("generated_encounters\\"+f_name, mode='w') as mon_export:
        mon_export.write("The following list of monsters has been "
                         "randomly generated:")
        for i in range(len(double_monster_list)):
            mon_export.write("\n{}. Please see {} for more information."
                             .format(double_monster_list[i][0],
                                     double_monster_list[i][-1]))
    print("")
    print("The following list of monsters has been randomly generated:")
    for i in range(len(double_monster_list)):
        print("{}. Please see {} for more information."
              .format(double_monster_list[i][0], double_monster_list[i][-1]))
    print("")
    print(r"The encounter has been saved in {}\generated_encounters\{}"
          .format(getcwd(), f_name))


def encounter_generator():
    levels = encounter_level_generator()
    print("How many monsters would you like to encounter?")
    print("Enter 1 for a single monster or 2 for multiple monsters.")
    encounter_size = ""
    while encounter_size != 1 or encounter_size != 2:
        try:
            encounter_size = int(input(""))
            if encounter_size == 1:
                get_solo_encounter(levels)
                break
            if encounter_size == 2:
                get_double_encounter(levels)
                break
            else:
                print("Please select one of the options by entering 1 or 2. ")
        except (ValueError, TypeError):
            print("Please enter 1 or 2.")
            pass

if __name__ == "__main__":

    print("")
    print("Welcome to Razdak's Dungeons and Dragons Fifth Edition random ")
    print("character and encouter generators. ")
    print("The Character generatore will generate up to 10 random characters.")
    print("The encounter generator generates encounters for 4-6 players")
    print("with a single monster or a group of monsters.")
    print("")
    print("Names were generated by the Dungeon and Dragons name generators ")
    print("at www.fantasynamegenerators.com \n \n ")

    pick_gen = 0
    while pick_gen != 1 or pick_gen != 2:
        try:
            pick_gen = int(input("Enter 1 for the character generator, "
                                 "or 2 for the encounter generator. "))
            print("")
            if pick_gen == 1 or pick_gen == 2:
                pass
            else:
                print("Please select one of the options by entering 1 or 2. ")
        except (ValueError, TypeError):
            print("Please enter 1 or 2.")
            pass
        if pick_gen == 1:
            char_generator()
            break
        if pick_gen == 2:
            encounter_generator()
            break

    print("\n")
    print("Wizards of the Coast, Dungeons & Dragons, D&D, and their logos ")
    print("are trademarks of Wizards of the Coast LLC in the United States ")
    print("and other countries. © 2019 Wizards. All Rights Reserved. These ")
    print("generators are not affiliated with, endorsed, sponsored, or ")
    print("specifically approved by Wizards of the Coast LLC.")
