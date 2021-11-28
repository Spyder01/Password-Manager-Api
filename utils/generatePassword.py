import string
import random

def generate_password (length):
    # characters to generate password from
    characters = list(string.ascii_letters+string.digits+ "!@#$%^&*()")

    # shuffling the characters
    length = int(length)

    # shuffling the characters
    random.shuffle(characters)

    # picking random characters from the list
    password = []

    for i in range(length):
        password.append(random.choice(characters))

    # shuffle his password
    random.shuffle(password)

    return "".join(password)



