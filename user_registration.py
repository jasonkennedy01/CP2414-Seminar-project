"""
Program to accept users registration using a computer generated password or user
entry and converting to a hash code.
"""
import hashlib
import json
import random
import re
import string
from types import SimpleNamespace

from account import Account

ACCOUNT_FILENAME = "accounts.dat"

MENU_STRING = "C)reate Account\nL)ogin\nQ)uit"


def main():
    """Display the menu and accept user input."""
    try:
        accounts = load_accounts_from_file(ACCOUNT_FILENAME)
    except FileNotFoundError:
        print("Accounts file not found...")
        accounts = []

    print(MENU_STRING)
    choice = input(">").upper()
    while choice != "Q":
        if choice == "C":
            create_account(accounts)
        if choice == "L":
            success = login(accounts)
            print(f"Login {success}.")
        print(MENU_STRING)
        choice = input(">").upper()

    print("Saving...")
    save_accounts_to_file(ACCOUNT_FILENAME, accounts)
    print("Saved.")


def create_account(accounts):
    """Add new account to accounts list."""
    username = input("Enter a username: ")

    choice = input("Generate random password? Y/n\n>").upper()
    if choice == 'N':
        password = input("Enter a password: ")
        while not is_valid_password(password):
            print("Password must contain")
            print("Lower case + Upper case + numbers + symbols + at least 8 characters")
            password = input("Enter a password: ")
    else:
        password = generate_random_password()
        print(password)

    print("How would you like to store your password?")
    encryption_method_choice = input("H)ash\nC)aeser\nR)SA\n>").upper()
    while encryption_method_choice not in 'HCR':
        print("How would you like to store your password?")
        encryption_method_choice = input("H)ash\nC)aeser\nR)SA\n>").upper()
    encryption_method = encryption_method_choice

    if encryption_method == 'H':
        cipher_key = input("Enter a cipher key: ")
        encrypted_password = hash_password(password, cipher_key)[0]

    # encrypted_password = encrypt_password(password, encryption_method)
    accounts.append(Account(username, encrypted_password, cipher_key))
    print(accounts)


def hash_password(password, salt=None):
    """Hash a password."""
    if salt is None:
        salt = str(random.uniform(100_000, 100_000_000))
    hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
    return hashed_password, salt


def pad_text(text, block_size=8):
    """Add padding to end of the text."""
    n = len(text) % block_size
    return text + (b' ' * (block_size - n))


def is_valid_password(text):
    """Check if text is valid password."""
    password_regex_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    return re.match(password_regex_pattern, text)


def load_accounts_from_file(filename):
    """Load accounts from file."""
    accounts = []
    with open(filename, 'rb') as in_file:
        for line in in_file:
            line = line.decode()
            if line != '\n':
                splits = line.split(' ')
                account = Account(splits[0].strip(), splits[2].strip(), splits[1].strip())
                accounts.append(account)
    return accounts


def save_accounts_to_file(filename, accounts):
    """Save accounts to file."""
    with open(filename, 'wb') as out_file:
        for account in accounts:
            out_file.write(account.username.encode())
            out_file.write(b' ')
            out_file.write(account.salt.encode())
            out_file.write(b' ')
            out_file.write(account.password.encode())
            out_file.write(b'\n')


def login(accounts):
    """Check username and password for valid credentials."""
    username = input("Username: ")
    for account in accounts:
        if account.username == username:
            password = input("Password: ")
            return compare_passwords(password, account.password, account.encryption_method)
    print("Account not found!")
    return False


def compare_passwords(input_password, stored_password, encryption_method):
    """Compare the given password and stored password."""
    pass


def generate_random_password(min_length=8, max_length=20):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(min_length, max_length))
    valid = is_valid_password(password)
    while not valid:
        password = ''.join(random.choice(characters) for i in range(min_length, max_length))
        valid = is_valid_password(password)
    return password


def encrypt_caesar_cipher(password, key):
    """Encrypt text based on a caeser rotation."""
    characters = list(string.ascii_letters + string.digits + string.punctuation)
    length_of_characters = len(characters)
    password_characters = list(password)
    for character_position, character in enumerate(password_characters):
        initial_index = characters.index(character)
        new_index = initial_index + key
        if new_index > length_of_characters - 1:
            new_index = 0 + (new_index - length_of_characters)
        password_characters[character_position] = characters[new_index]
    password_cypher = "".join(password_characters)
    return password_cypher


def decrypt_caesar_cipher(password, key):
    """Decrypt text based on a caeser rotation."""
    characters = list(string.ascii_letters + string.digits + string.punctuation)
    length_of_characters = len(characters)
    password_characters = list(password)
    for character_position, character in enumerate(password_characters):
        initial_index = characters.index(character)
        new_index = initial_index - key
        if new_index < 0:
            new_index = length_of_characters - (key - initial_index)
        password_characters[character_position] = characters[new_index]
    password_cypher = "".join(password_characters)
    return password_cypher


if __name__ == '__main__':
    main()
