import character_generator

class PasswordGenerator(object):
    def __init__(self):
        pass

    def generate(self, length=14):
        generator = character_generator.CharacterGenerator()
        password = []

        while len(password) != length:
            password.append( generator.generate() )

        return "".join(password)

if __name__ == "__main__":
    passGen = PasswordGenerator()
    print(passGen.generate(25))