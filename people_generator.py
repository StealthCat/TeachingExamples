import random

class NoNamesException(Exception):
    pass

class DuplicateNameException(Exception):
    pass

class Person(object):

    people = {}
    names = ['Steve', 'Joe', 'Ted', 'Fred', 'Frank', 'Batman']

    def __init__(self, name=False, age=False):

        if not name:
            name = random.choice(Person.names)
            triedNames = 1

            while Person.find(name) != None and triedNames < len(Person.names):
                name = random.choice(Person.names)
                triedNames += 1
            
            if triedNames > len(Person.names):
                raise NoNamesException

        elif Person.find(name) != None:
            raise DuplicateNameException

        if not age:
            age = random.randint(0,100)

        self.name = name
        self.age = age

        Person.people[self.name] = self

    def __repr__(self):
        return "Person({0!r}, {1})".format(self.name, self.age)

    def __str__(self):
        return self.name

    def find(name):
        return Person.people.get(name)

    def age(name, years):
        Person.find(name).age += years

    def kill(name):
        if Person.people.get(name) != None:
            del Person.people[name]
        else:
            raise KeyError

def PeopleGenerator(population=False, names=False):
    if not population and names:
        population = len(names)

    if not population:
        raise ValueError("Population non-numeric")

    for i in range(population):
        if names:
            yield Person(names[i])
        else:
            yield Person()

for person in PeopleGenerator(names=Person.names):
    print(f"Creating {person.name}")

name = " "
while name:
    name = input("Please enter character name: ")

    if name:
        try:
            Person(name)
        except DuplicateNameException:
            print("That name is already in use, please try again.")

print(Person.people)