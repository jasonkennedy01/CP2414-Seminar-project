"""An account module."""


class Account:
    """An account"""

    def __init__(self, username, password, salt=None):
        self.username = username
        self.password = password
        self.salt = salt

    def __str__(self):
        return f"Account {self.username} [{self.password}, {self.salt}]"

    def __repr__(self):
        return self.__str__()
