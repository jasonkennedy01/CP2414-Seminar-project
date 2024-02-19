"""
Program to accept users registration using a computer generated password or user
entry and converting to a hash code.
"""
import hashlib
import random
import re
import string

MENU_STRING = "C)reate Account\nL)ogin\nQ)uit"


def main():
    """Display the menu and accept user input."""
    accounts = load_accounts_from_file("accounts.txt")

    print(MENU_STRING)
    choice = input(">").upper()
    while choice != "Q":
        if choice == "C":
            create_account(accounts)
        if choice == "L":
            login(accounts)
        print(MENU_STRING)
        choice = input(">").upper()
    save_accounts_to_file("accounts.txt", accounts)


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

    accounts[username] = hash_password(password)
    print(accounts)


def hash_password(password, salt=None):
    """Hash a password."""
    if salt is None:
        salt = str(random.uniform(100_000, 100_000_000))
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password, salt


def is_valid_password(text):
    """Check if text is valid password."""
    password_regex_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    if re.match(password_regex_pattern, text):
        return True
    return False


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


if __name__ == '__main__':
    main()
