"""An account module."""


class Account:
    """An account"""

    def __init__(self, username, password, encryption_method):
        self.username = username
        self.password = password
        self.encryption_method = encryption_method

    def __str__(self):
        return f"Account {self.username} [{self.password}, {self.encryption_method}]"

    def __repr__(self):
        return self.__str__()
