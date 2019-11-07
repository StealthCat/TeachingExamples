import character_generator

class PasswordLengthException(Exception):
    pass

class PasswordGenerator(object):
    def __init__(self):
        pass

    def generate(self, length=14):

        if length < 14:
            raise PasswordLengthException("Password length requirement not met")

        generator = character_generator.CharacterGenerator()
        password = []

        while len(password) != length:
            password.append( generator.generate() )

        return "".join(password)

if __name__ == "__main__":
    while True:
        try:
            passLen = int(input("Please enter the password length: "))
            
            passGen = PasswordGenerator()
            password = passGen.generate(passLen)

        except ValueError:
            print("You did not enter a number, please try again.")
        except PasswordLengthException as ex:
            print(ex)
        except KeyboardInterrupt:
            print("lol...no")
        else:
            print("Your password is: {}".format(password))
            break

