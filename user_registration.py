"""Program to accept users registration using a computer generated password or user
entry and converting to a hash code."""
import random
import string

def main():
    pass


def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(random.randint(8,20)))



    return password

def get_user_password():
    pass


def convert_to_hash():
    pass


def save_to_file():
    pass


# main()
print(generate_random_password())