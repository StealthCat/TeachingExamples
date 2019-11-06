import random
import string

class CharacterGenerator(object):
    def __init__(self):
        self.categories = { 'U': string.ascii_uppercase, 
                            'L': string.ascii_lowercase, 
                            'D': string.digits,
                            'P': string.punctuation }
        self.required = {category:True for category in self.categories}
        self.contains = {category:False for category in self.categories}
        self.history = [None, None, None]

    def generate(self):
        success = False
        while not success:
            choices = []
            for category in self.contains:
                if not self.contains[category]:
                    choices.append(category)

            if not choices:
                choices = list(self.categories.keys())

            category = random.choice(choices)

            if set(self.history) != set(category):
                self.history.append(category)
                self.history.pop(0)
                self.contains[category] = True

                choice = random.choice(self.categories[category])
                success = True

        return choice

if __name__ == "__main__":
    gen = CharacterGenerator()
    password = []

    for i in range(random.randint(14,26)):
        password.append(gen.generate())
    print("".join(password))