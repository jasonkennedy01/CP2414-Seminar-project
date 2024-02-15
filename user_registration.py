"""Program to accept users registration using a computer generated password or user
entry and converting to a hash code."""


def main():
    pass


def generate_random_password():
    pass


def get_user_password(password):
    password_characters = list(password)
    lowercase_characters = [character for character in password_characters if character.islower()]
    uppercase_characters = [character for character in password_characters if character.isupper()]
    numbers = [number for number in password_characters if number.isnumeric()]

    while len(password_characters) < 8 and len(lowercase_characters) <= 0 and len(numbers) <= 0 :
        print("Invalid Password: Too short")


def convert_to_hash():
    pass


def save_to_file():
    pass


main()