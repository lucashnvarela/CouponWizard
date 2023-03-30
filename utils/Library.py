import json
import re


class Library:
    """ A library of coupons and user credentials data """

    def __init__(self):
        """ Initializes a new instance of the Library class """

        self.log_file = "log.json"
        self.credentials_file = "user_credentials.json"

        self.log = self.load_file(file_name=self.log_file)
        self.user_credentials = self.load_file(file_name=self.credentials_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.update_files()

    def load_file(self, file_name: str) -> dict:
        """ 
        Loads a JSON file containing data, or returns an empty dictionary 

        :param file_name: Name of the JSON file to load
        :returns: Dictionary with the data from the JSON file
        or an empty dictionary if the file does not exist or is empty
        """

        try:
            with open(file_name) as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return dict()

    def update_files(self) -> None:
        """ 
        Writes the current data to their respective JSON files 

        :returns: None
        """

        with open(self.log_file, "w+") as file:
            json.dump(self.log, file)

        with open(self.credentials_file, "w+") as file:
            json.dump(self.user_credentials, file)

    def filter_coupons(self, coupons: list) -> list:
        """ 
        Filters out any coupons that have already been added to the coupons log

        :param coupons: List with coupons to filter
        :returns: List with coupons that are not already in the coupons log
        """

        new_coupons = list()

        for coupon in coupons:
            if coupon not in self.log.keys():
                new_coupons.append(coupon)

        return new_coupons

    def add_coupons(self, coupons: dict) -> None:
        """
        Adds the given dictionary of coupons to add to the coupons log

        :param coupons: Dictionary with coupon codes to add
        :returns: None
        """

        self.log.update(coupons)

    def get_user_credentials(self) -> dict:
        """ 
        Returns the user credentials from the user_credentials attribute

        :returns: List with the user credentials
        """

        email_pattern = re.compile(
            r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$")

        steam_credentials = list(self.user_credentials["steam"].values())
        pa_credentials = list(self.user_credentials["pearl_abyss"].values())

        if sum(bool(value) for value in steam_credentials) >= 2:

            steam_pp = self.user_credentials["steam"]["pp_pin"]

            if steam_pp:
                if len(steam_pp) != 4:
                    raise Exception("Invalid parental protection pin")

            return {"steam": steam_credentials}

        elif sum(bool(value) for value in pa_credentials) == 2:

            if not re.match(email_pattern, self.user_credentials["pearl_abyss"]["email"]):
                raise Exception("Invalid email address")

            return {"pearl_abyss": pa_credentials}

        else:
            raise Exception("No user credentials provided")

    def save_user_credentials(self, user_credentials: dict) -> None:
        """ 
        Saves the user credentials to the user_credentials attribute

        :param credentials: Dictionary with the user credentials
        :returns: None
        """

        self.user_credentials.update(user_credentials)
