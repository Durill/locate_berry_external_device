from re import match
from getpass import getpass

__all__ = ("UserInputHandler",)


class UserInputHandler:
    EMAIL_PATTER = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    MINIMUM_PASSWORD_LENGTH = 5

    @classmethod
    def email_input(cls) -> str:
        email: str = input("Enter your email: ")
        while True:
            if match(cls.EMAIL_PATTER, email):
                break

            email = input("Email is not valid, enter your email again: ")

        return email

    @classmethod
    def password_input(cls) -> str:
        password: str
        while True:
            password = getpass(prompt="Password: ")
            if len(password) > cls.MINIMUM_PASSWORD_LENGTH:
                break

            print(f"Password must be at least {cls.MINIMUM_PASSWORD_LENGTH} characters long")

        return password
