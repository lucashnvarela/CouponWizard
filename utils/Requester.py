import requests


class Requester:
    """ Requests active coupons from the Garmoth API """

    API = "https://garmoth.com/api/coupons"
    HEADERS = {"User-Agent": "CouponWizard"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def parse_coupons(self, response: dict) -> list:
        """ 
        Retrieves coupon codes from the JSON response

        :param response: JSON response from the API
        :returns: List with coupon codes
        """

        coupons = list()

        for coupon in response:
            coupons.append(coupon["code"])

        return coupons

    def request_coupons(self) -> list:
        """ 
        Sends a GET request to the API and returns a list with coupons

        :returns: List with coupons
        """

        response = requests.get(url=self.API, headers=self.HEADERS)
        response.raise_for_status()

        return self.parse_coupons(response=response.json())
