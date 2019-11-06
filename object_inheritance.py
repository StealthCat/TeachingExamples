
class Person(object):
    def __init__(self, name, age, title=None):
        self.name = name
        self.age = age
        self.title = title

    def __repr__(self):
        if self.title != None:
            return "Person('{}', {}, title='{}')".format(
                            self.name, self.age, self.title)
        else:
            return "Person('{}', {})".format(self.name, self.age)
       
    def __lt__(self, other):
        if type(other) != Person:
            return False
        if type(other) == SuperHero:
            return True
        if other.title == None and self.title != None:
            return False
        return self.age < other.age
        

    def __eq__(self, other):
        return self.age == other.age


    def talk(self):
        if self.title != None:
            print("I am " + self.title + " " + self.name)
        else:
            print("I am " + self.name)

    def birthday(self):
        self.age += 1

    def freeze(self, years):
        self.age += years

    def powerup(self):
        newObj = SuperHero(self.name, self.age)
        self.__class__ = newObj.__class__
        self.__dict__.clear()
        self.__dict__.update(newObj.__dict__)

class SuperHero(Person):
    def __init__(self, name, age, title=None, secret=None):
        Person.__init__(self, name, age, title)
        self.secret = secret   

Steve = SuperHero("Steve", 42, title="Captain", secret="Captain America")
Ted = Person("Steve", 42, title="Captain")
Adam = Person("Adam", 16)
Adam2 = Person("Adam", 18)

print(type(Steve) == type(Adam))
print(Steve == Adam)

Steve.talk()
Adam.talk()