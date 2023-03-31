import logging

from utils.Library import Library


def setup() -> None:
    """ 
    Setup function to save user credentials for their chosen account provider

    :returns: None
    """

    def setup_steam() -> None:
        """
        Save Steam account credentials

        :returns: None
        """

        print("\nSteam account credentials")
        username = input("Username: ")
        password = input("Password: ")
        pp_pin = input(
            "Parental protection pin: ")

        save_credentials(
            {"steam": {"username": username, "password": password, "pp_pin": pp_pin}})

    def setup_pearl_abyss() -> None:
        """
        Save Pearl Abyss account credentials

        :returns: None
        """

        print("\nPearl Abyss account credentials")
        email = input("Email: ")
        password = input("Password: ")

        save_credentials(
            {"pearl_abyss": {"email": email, "password": password}})

    def save_credentials(user_credentials: dict) -> None:
        """
        Save user credentials to the JSON file

        :param user_credentials: Dictionary with user credentials
        :returns: None
        """

        with Library() as library:
            library.save_user_credentials(user_credentials=user_credentials)

    while True:
        print("\nPlease choose your account provider:")
        print("  1. Steam")
        print("  2. Pearl Abyss\n")

        account_provider = input(":")

        switch = {
            "1": lambda: setup_steam(),
            "2": lambda: setup_pearl_abyss()
        }

        try:
            switch[account_provider]()
            logging.info("User credentials file updated.")
            break

        except KeyError:
            logging.error("Invalid option.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    setup()
