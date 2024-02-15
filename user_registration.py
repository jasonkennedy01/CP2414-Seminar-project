"""Program to accept users registration using a computer generated password or user
entry and converting to a hash code."""

import hashlib
import random
import string

MENU = (f"C)REATE ACCOUNT\n"
        f"L)OGIN\n"
        f"Q)UIT\n")


def main():
    print(MENU)
    choice = input(">").upper()
    while choice != "Q":
        if choice == "C":
            create_account()
        if choice == "L":
            login()
        choice = input(">").upper()


def create_account():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    while not is_valid_password(password):
        password = input("Enter your password: ")
    # save_to_file()
    print("Account created successfully!")


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    # check username exists
    # check password against username
    # print success
    # print failure


def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation


def is_valid_password(password):
    password_characters = list(password)
    lowercase_characters = [character for character in password_characters if character.islower()]
    uppercase_characters = [character for character in password_characters if character.isupper()]
    numbers = [number for number in password_characters if number.isnumeric()]

    while len(password_characters) < 8 and len(lowercase_characters) <= 0 and len(numbers) <= 0:
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
    # test()
    main()
