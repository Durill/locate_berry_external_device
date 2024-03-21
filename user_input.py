from re import match


class UserInput:
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    @classmethod
    def email_input(cls) -> str:
        email: str = input("Enter your email: ")
        while True:
            if match(cls.email_pattern, email):
                break

            email = input("Email is not valid, enter your email again: ")

        return email

    @classmethod
    def device_name_input(cls) -> str:
        name: str = input("Enter name for this device: ")
        while True:
            if 3 <= len(name) <= 25:
                break

            name = input("Name have to have length between 3 and 25 characters, try again: ")

        return name
