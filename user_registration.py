"""Program to accept users registration using a computer generated password or user
entry and converting to a hash code."""

import hashlib
import random


def main():
    pass


def generate_random_password():
    pass


def get_user_password():
    pass


def convert_to_hash(text, salt):
    sha256 = hashlib.sha256()
    sha256.update((text + str(salt)).encode())
    return sha256.hexdigest()


def save_to_file():
    pass


def generate_salt():
    return random.uniform(1_000, 100_000_000)


def test():
    print("Alpha@01, 12834\t", convert_to_hash("Alpha@01", 12834))
    print("Alpha@01, 93834\t", convert_to_hash("Alpha@01", 93834))
    print("Alpha@02, 93849\t", convert_to_hash("Alpha@02", 93849))
    print("Alpha@02, 93849\t", convert_to_hash("Alpha@02", 93849))
    print("Alpha@02, generate_salt()\t", convert_to_hash("Alpha@02", generate_salt()))


if __name__ == '__main__':
    test()
    main()
