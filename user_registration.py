"""
Program to accept users registration using a computer generated password or user
entry and converting to a hash code.
"""
import hashlib
import random
import re
import string
from Crypto.Cipher import DES
from account import Account

MENU_STRING = "C)reate Account\nL)ogin\nQ)uit"
# To-Do: Load keys from file and generate on first run
DES_KEY = 'aCP2414a'
CAESER_KEY = 'CP2414'


def main():
    """Display the menu and accept user input."""
    try:
        accounts = load_accounts_from_file("accounts.txt")
    except FileNotFoundError:
        print("Accounts file not found...")
        accounts = []

    print(MENU_STRING)
    choice = input(">").upper()
    while choice != "Q":
        if choice == "C":
            create_account(accounts)
        if choice == "L":
            login(accounts)
        print(MENU_STRING)
        choice = input(">").upper()

    print("Saving...")
    save_accounts_to_file("accounts.txt", accounts)
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
    encryption_method_choice = input("H)ash\nC)aeser\nD)ES").upper()
    while encryption_method_choice not in 'HCD':
        print("How would you like to store your password?")
        encryption_method_choice = input("H)ash\nC)aeser\nD)ES").upper()
    encryption_method = encryption_method_choice

    encrypted_password = encrypt_password(password, encryption_method)
    accounts.append(Account(username, encrypted_password, encryption_method))
    print(accounts)


def encrypt_password(password, encryption_method='H'):
    """Return an encrypted password based on a provided encryption method."""
    if encryption_method == 'H':
        return hash_password(password)
    if encryption_method == 'C':
        return encrypt_caesar_cipher(password, CAESER_KEY)
    if encryption_method == 'D':
        return encrypt_des(DES_KEY, password)
    return None


def hash_password(password, salt=None):
    """Hash a password."""
    if salt is None:
        salt = str(random.uniform(100_000, 100_000_000))
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password, salt


def encrypt_des(key, plaintext):
    """Encrypt text using DES encryption."""
    des = DES.new(key.encode(), DES.MODE_ECB)
    padded_text = pad_text(plaintext.encode())
    encrypted_text = des.encrypt(padded_text)
    return encrypted_text


def decrypt_des(key, encrypted_text):
    """Decrypt text using DES encryption."""
    des = DES.new(pad_text(key.encode('utf-8')), DES.MODE_ECB)
    plaintext = des.decrypt(encrypted_text)
    return plaintext.decode('utf-8').strip()


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
    accounts = {}
    with open(filename, 'r', encoding='utf-8') as in_file:
        for line in in_file:
            items = line.split()
            accounts[items[0]] = (items[1], items[2])
    return accounts


def save_accounts_to_file(filename, accounts):
    """Save accounts to file."""
    with open(filename, 'w', encoding='utf-8') as out_file:
        for account in accounts:
            out_file.write(f"{account} {accounts[account][0]} {accounts[account][1]}\n")


def login(accounts):
    """Check username and password for valid credentials."""
    username = input("Username: ")
    if username not in accounts.keys():
        print("Account does not exist")
        return
    password = input("Password: ")
    hashed_password, salt = accounts[username]
    if hash_password(password, salt)[0] == hashed_password:
        print("Logged in successfully")
    else:
        print("Incorrect password!!!")


def generate_random_password():
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(random.randint(8, 20)))
    valid = is_valid_password(password)
    while not valid:
        password = ''.join(random.choice(characters) for i in range(random.randint(8, 20)))
        valid = is_valid_password(password)
    return password


def encrypt_caesar_cipher(password, key):
    """Method is still broken"""
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
    print(encrypt_des(DES_KEY, 'a'))
    main()
