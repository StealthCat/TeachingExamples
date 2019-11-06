import string

required_types = set(['L','D','U','P'])

def characterize(character):
    if character in string.ascii_uppercase:
        return 'U'
    if character in string.ascii_lowercase:
        return 'L'
    if character in string.digits:
        return 'D'
    else:
        return 'P'

def password_check(password):
    password_array = [characterize(character) for character in password]
    if required_types != set(password_array):
        print("Failed: Missing type: {}".format(",".join(required_types-set(password_array))))
        return False

    for i in range(len(password_array)):
        if len(set(password_array[i:i+4])) == 1:
            print("Failed: ", password[i:i+4])
            return False

password = 'ATestPasswordOfDoom!2'
password_check(password)
