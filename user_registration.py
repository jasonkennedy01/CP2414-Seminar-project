"""
Program to accept users registration using a computer generated password or user
entry and converting to a hash code.
"""
import hashlib
import json
import random
import re
import string
<<<<<<< HEAD
import secrets
=======
from types import SimpleNamespace

>>>>>>> 96bce5f903ef99e9b3a5eea7730feb468fa67632
from Crypto.Cipher import DES
from account import Account

ACCOUNT_FILENAME = "accounts.json"
KEYS_FILENAME = "secrets.txt"

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
    encryption_method_choice = input("H)ash\nC)aeser\nD)ES\n>").upper()
    while encryption_method_choice not in 'HCD':
        print("How would you like to store your password?")
        encryption_method_choice = input("H)ash\nC)aeser\nD)ES\n>").upper()
    encryption_method = encryption_method_choice

    encrypted_password = encrypt_password(password, encryption_method)
    accounts.append(Account(username, encrypted_password, encryption_method))
    print(accounts)


def encrypt_password(password, encryption_method='H'):
    """Return an encrypted password based on a provided encryption method."""
    if encryption_method == 'H':
        return hash_password(password)
    if encryption_method == 'C':
        return encrypt_caesar_cipher(password, int(CAESER_KEY))
    if encryption_method == 'D':
        return encrypt_des(DES_KEY, password)
    return None


def decrypt_password(password, encryption_method='H'):
    """Return a decrypted password based on a provided encryption method."""
    if encryption_method == 'H':
        return hash_password(password)
    if encryption_method == 'C':
        return encrypt_caesar_cipher(password, int(CAESER_KEY))
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
    des = DES.new(key.encode('ascii'), DES.MODE_ECB)
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
    accounts = []
    with open(filename, 'rb') as in_file:
        accounts = json.load(in_file, object_hook=lambda x: SimpleNamespace(**x))
    return accounts


def create_keys_file(filename):
    """Create keys."""
    with open(filename, 'w') as out_file:
        out_file.write(generate_random_password(max_length=8) + '\n')  # DES KEY, generate password returns a block of 8 chars
        out_file.write(str(random.randint(0, 26)))  # CAESER KEY


def save_accounts_to_file(filename, accounts):
    """Save accounts to file."""
    with open(filename, 'w') as out_file:
        out_file.write(json.dumps(accounts, default=vars))


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
    if encryption_method == 'H':
        print(hash_password(input_password, stored_password[1]))
        print(stored_password[0])
        return hash_password(input_password, stored_password[1])[0] == stored_password[0]
    if encryption_method == 'C':
        return encrypt_caesar_cipher(input_password, int(CAESER_KEY)) == stored_password
    if encryption_method == 'D':
        return encrypt_des(DES_KEY, input_password) == stored_password
    return False


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


<<<<<<< HEAD
def generate_secret_value(length):
    """Generate a random secret value of given length"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))




=======
def load_keys_from_file(filename):
    try:
        with open(filename, 'r', encoding='ascii') as in_file:
            keys = in_file.readlines()
            for i in range(len(keys)):
                keys[i] = keys[i].strip()
        return keys
    except FileNotFoundError:
        create_keys_file(filename)
    return load_keys_from_file(filename)


DES_KEY, CAESER_KEY = load_keys_from_file(KEYS_FILENAME)
>>>>>>> 96bce5f903ef99e9b3a5eea7730feb468fa67632

if __name__ == '__main__':
    main()
