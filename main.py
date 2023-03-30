import logging

from utils.Bot import Bot
from utils.Library import Library
from utils.Requester import Requester


def main() -> None:
    """
    Main function to execute the script

    :returns: None
    """

    with Requester() as requester:
        with Library() as library:

            try:
                # Retrieve the user credentials from the JSON file
                user_credentials = library.get_user_credentials()

            # if the credentials were not provided,
            # end the script
            except Exception as e:
                logging.error(e)
                return

            logging.info("Requesting coupons")

            try:
                # Retrieve the current active coupons from the API
                # and filter out the coupons that have already been redeemed
                new_coupons = library.filter_coupons(
                    coupons=requester.request_coupons())

            # If the request failed,
            # end the script
            except Exception as e:
                logging.error(e)
                return

            # If there are no new coupons,
            # end the script
            if not new_coupons:
                logging.info("No new coupons to redeem")
                return

            logging.info(f"Found {len(new_coupons)} new coupons to redeem")

    with Bot() as bot:

        try:
            # Login in to Steam account using the provided username and password
            if user_credentials["steam"]:
                logging.info("Logging in to Steam account")
                bot.steam_account_login(*user_credentials["steam"])

            # Login in to Pearl Abyss account using the provided email and password
            elif user_credentials["pearl_abyss"]:
                logging.info("Logging in to Pearl Abyss account")
                # TODO: Add support for PA account login
                bot.pa_account_login(*user_credentials["pearl_abyss"])

        # If the login attempt failed,
        # end the script
        except Exception as e:
            logging.error(e)
            return

        # If the login was successful,
        # redeem the coupons
        logging.info("Redeeming coupons")

        coupons_log = dict()

        try:
            # Attempt to redeem the coupons and add them to the log
            for coupon in new_coupons:
                coupons_log.update(bot.redeem_coupon(coupon=coupon))

        # If the attempt failed,
        # end the script
        except Exception as e:
            logging.error(e)
            return

        # print the ratio of coupons redeemed
        success_count = list(coupons_log.values()).count("Success")
        logging.info(f"{success_count}/{len(new_coupons)} coupons redeemed")

        with Library() as library:

            # Add the coupons to the log file
            library.add_coupons(coupons=coupons_log)

        logging.info("Log file updated")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    main()
