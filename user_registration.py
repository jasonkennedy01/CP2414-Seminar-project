"""Program to accept users registration using a computer generated password or user
entry and converting to a hash code."""

import hashlib
import random

import random
import string

def main():
    pass


def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation


def get_user_password(password):
    password_characters = list(password)
    lowercase_characters = [character for character in password_characters if character.islower()]
    uppercase_characters = [character for character in password_characters if character.isupper()]
    numbers = [number for number in password_characters if number.isnumeric()]

    while len(password_characters) < 8 and len(lowercase_characters) <= 0 and len(numbers) <= 0 :
        print("Invalid Password: Too short")


def generate_hash(text, salt):
    sha256 = hashlib.sha256()
    sha256.update((text + str(salt)).encode())
    return sha256.hexdigest()


def save_to_file():
    pass


def generate_salt():
    return random.uniform(1_000, 100_000_000)


def test():
    print("Alpha@01, 12834\t", generate_hash("Alpha@01", 12834))
    print("Alpha@01, 93834\t", generate_hash("Alpha@01", 93834))
    print("Alpha@02, 93849\t", generate_hash("Alpha@02", 93849))
    print("Alpha@02, 93849\t", generate_hash("Alpha@02", 93849))
    print("Alpha@02, generate_salt()\t", generate_hash("Alpha@02", generate_salt()))


if __name__ == '__main__':
    test()
    main()
