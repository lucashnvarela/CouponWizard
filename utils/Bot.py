import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Bot:
    """ Submits coupons to the BlackDesert website """

    LOGIN_PAGE = "https://account.pearlabyss.com/Member/Login"
    COUPON_REDEEM_PAGE = "https://payment.naeu.playblackdesert.com/en-US/Shop/Coupon/"

    def __init__(self):
        """ Initializes webdriver options and create a webdriver instance """

        self.webdriver_options = webdriver.ChromeOptions()
        # Run selenium in headless mode
        self.webdriver_options.add_argument(argument="--headless")
        # Hide console logs
        self.webdriver_options.add_experimental_option(
            name="excludeSwitches", value=["enable-logging"])
        self.webdriver = webdriver.Chrome(options=self.webdriver_options)

        # Set webdriver wait times
        self.short_wait = WebDriverWait(driver=self.webdriver, timeout=5)
        self.wait = WebDriverWait(driver=self.webdriver, timeout=15)

        self.webdriver.get(url=self.LOGIN_PAGE)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.webdriver.quit()

    def steam_account_login(self, username: str, password: str, pp_pin: str) -> None:
        """
        Login to Steam account using provided username, password

        :param username: Steam account username
        :param password: Steam account password
        :param pp_pin: Steam parental protection pin (optional)
        :return: None
        """

        STEAM_SELECTORS = {
            "pa_navbar": ".bg_top_newtwork",
            "steam_button": ".btn_steam_login",
            "login_form": ".newlogindialog_LoginForm_3Tsg9 input",
            "login_submit_button": ".newlogindialog_SubmitButton_2QgFE",
            "login_timeout": ".newlogindialog_FailureTitle_A3Y-u",
            "auth_page": ".newlogindialog_ConfirmationContainer_2aZnk",
            "auth_code_button": ".newlogindialog_EnterCodeInsteadLink_37AOB",
            "auth_form": ".newlogindialog_FormContainer_3jLIH input",
            "auth_done": ".throbber_Throbber_7MdwT",
            "pp_input": "#steam_parental_password_box",
            "pp_submit_button": "#submit_btn",
            "pp_error": "#parental_error",
            "signin_button": "#imageLogin",
            "error": ".newlogindialog_Danger_1-HwJ"
        }

        try:
            # Wait for the login page to load
            self.wait.until(
                method=expected_conditions.presence_of_all_elements_located(
                    locator=(By.CSS_SELECTOR, STEAM_SELECTORS["pa_navbar"])))

            # Click the steam login button
            steam_button = self.webdriver.find_element(
                By.CSS_SELECTOR, STEAM_SELECTORS["steam_button"])

            # Javascript click to avoid element not interactable exception
            self.webdriver.execute_script(
                "arguments[0].click();", steam_button)

        # If the steam login page is unreachable,
        # raise an exception
        except TimeoutException:
            raise Exception("Steam login page unreachable")

        try:
            # Wait for the login form to load
            login_form = self.wait.until(
                method=expected_conditions.presence_of_all_elements_located(
                    locator=(By.CSS_SELECTOR, STEAM_SELECTORS["login_form"])))

        # If the steam login form is not found,
        # raise an exception
        except TimeoutException:
            raise Exception("Steam login form not found")

        # Fill in the login form with the provided username and password
        for login_input, login_data in zip(login_form, [username, password]):
            login_input.send_keys(login_data)

        # Click the login button
        self.webdriver.find_element(
            By.CSS_SELECTOR, STEAM_SELECTORS["login_submit_button"]).click()

        try:
            # Wait for the authentication page to load
            self.short_wait.until(
                method=expected_conditions.presence_of_all_elements_located(
                    locator=(By.CSS_SELECTOR, STEAM_SELECTORS["auth_page"])))

            # If the authentication page is found,
            # print login is successful
            logging.info("Login successful")

        # If the authentication page is not found,
        # check for error message or login timeout
        except TimeoutException:
            try:
                # Wait for an error message to appear
                self.short_wait.until(
                    method=expected_conditions.presence_of_all_elements_located(
                        locator=(By.CSS_SELECTOR, STEAM_SELECTORS["error"])))

                # If an error message is found,
                # raise an exception
                raise Exception("Invalid username or password")

            # If no error message is found,
            # check for login timeout
            except TimeoutException:
                try:
                    # Check for login timeout
                    self.short_wait.until(
                        method=expected_conditions.presence_of_element_located(
                            locator=(By.CSS_SELECTOR, STEAM_SELECTORS["login_timeout"])))

                    # If login timeout is found,
                    # raise an exception
                    raise Exception("Login timeout, please try again later")

                # If either error message or login timeout is not found,
                # raise an exception
                except TimeoutException:
                    raise Exception("Authentication page unreachable")

        try:
            logging.info("Waiting for authentication confirmation")

            # Wait for the authentication to be accepted
            self.wait.until(
                method=expected_conditions.presence_of_element_located(
                    locator=(By.CSS_SELECTOR, STEAM_SELECTORS["auth_done"])))

            logging.info("Authentication successful")

        # If the authentication is not accepted,
        # raise an exception
        except TimeoutException:
            raise Exception("Authentication timeout")

        try:
            # Wait for the parental protection form to load
            pp_input = self.short_wait.until(
                method=expected_conditions.presence_of_element_located(
                    locator=(By.CSS_SELECTOR, STEAM_SELECTORS["pp_input"])))

            # If no parental protection pin is provided,
            # raise an exception
            if not pp_pin:
                raise Exception("Parental protection pin not provided")

            # Fill in the parental protection pin
            pp_input.send_keys(pp_pin)

            # Check for incorrect pin message
            pp_error = self.webdriver.find_element(
                By.CSS_SELECTOR, STEAM_SELECTORS["pp_error"])

            # If the parental protection pin is incorrect,
            # raise an exception
            if len(pp_error.text) > 0:
                raise Exception("Parental protection pin incorrect")

            # Click the submit button
            self.webdriver.find_element(
                By.CSS_SELECTOR, STEAM_SELECTORS["pp_submit_button"]).click()

        # If the parental protection form is unreachable,
        # assume that parental protection is not enabled
        except TimeoutException:
            pass

        # Click the sign in button
        self.short_wait.until(
            method=expected_conditions.presence_of_element_located(
                locator=(By.CSS_SELECTOR, STEAM_SELECTORS["signin_button"]))).click()

        # Wait for the profile page to load
        self.wait.until(
            method=expected_conditions.presence_of_all_elements_located(
                locator=(By.CSS_SELECTOR, STEAM_SELECTORS["pa_navbar"])))

    def pa_account_login(self, email: str, password: str) -> None:
        """ 
        Login to Pear Abyss account using the provided email and password

        :param email: PA account email
        :param password: PA account password
        :return: None
        """

        pass

    def redeem_coupon(self, coupon: str) -> dict:
        """
        Redeem a coupon code and returns a dictionary with the coupon code and status

        :param coupon: The coupon code to redeem
        :return: A dictionary with the coupon code and its status
        """

        REDEEM_SELECTORS = {
            "pa_navbar": ".bg_top_newtwork",
            "coupon_form": ".custom_input input",
            "submit_button": "#submitCoupon",
        }

        def redeem_alert_handler() -> str:
            """
            Helper function to handle the alert that appears after redeeming a coupon

            :return: The status of the coupon redeemed
            """
            SUBMIT_DIALOG = {
                "Success": "You have successfully redeemed the coupon code.",
                "Already Redeemed": "This coupon code cannot be used multiple times.",
                "Invalid": "You cannot use this coupon code."
            }

            # Wait for the alert to load
            alert = self.short_wait.until(
                method=expected_conditions.alert_is_present())

            # Check for the status of the coupon redeem
            for status, message in SUBMIT_DIALOG.items():
                if message in alert.text:
                    alert.accept()
                    return status

            # If no status was found,
            # raise an exception
            raise Exception("Coupon redeem timeout")

        # Navigate to the coupon redeem page
        self.webdriver.get(url=self.COUPON_REDEEM_PAGE)

        try:
            # Check if its the correct page
            self.wait.until(
                method=expected_conditions.url_contains(
                    url="Shop/Coupon"))

            # Wait for the coupon redeem page to load
            self.wait.until(
                method=expected_conditions.presence_of_element_located(
                    locator=(By.CSS_SELECTOR, REDEEM_SELECTORS["pa_navbar"])))

        # If the coupon redeem page is unreachable,
        # raise an exception
        except TimeoutException:
            raise Exception("Coupon redeem page unreachable")

        # Find the input fields for the coupon code
        coupon_form = self.webdriver.find_elements(
            By.CSS_SELECTOR, REDEEM_SELECTORS["coupon_form"])

        # Fill in the coupon code
        for coupon_input, coupon_slice in zip(coupon_form, coupon.split("-")):
            coupon_input.send_keys(coupon_slice)

        # Click the submit button
        submit_button = self.webdriver.find_element(
            By.CSS_SELECTOR, REDEEM_SELECTORS["submit_button"])

        # Javascript click to avoid element not interactable exception
        self.webdriver.execute_script("arguments[0].click();", submit_button)

        # Handle any alert that appears after redeeming the coupon
        status = redeem_alert_handler()

        # If the coupon was already redeemed or invalid,
        # return a dictionary with the coupon code and status
        if status != "Success":
            return {coupon: status}

        try:
            # Wait for the confirmation page to load
            self.wait.until(
                method=expected_conditions.url_contains(
                    url="WebItemStorage/Complete"))

            return {coupon: status}

        # If the confirmation page is unreachable,
        # raise an exception
        except TimeoutException:
            raise Exception("Redeem confirmation page unreachable")
