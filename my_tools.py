# This file contains code snippits that can be imported into other projects
from getpass import getpass


def get_credentials():
    """This function Prompts you for a username and password and returns a username and password"""
    username = input('Enter Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match. Try again.')
            password = None
    return username, password


if __name__ == "__main__":
    print("my_tools.py is running directly...")
    get_credentials()