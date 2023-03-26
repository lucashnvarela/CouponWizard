import requests


class CouponRequester:
    api_url = "https://garmoth.com/api/coupons"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def get_response(self):
        headers = {"User-Agent": "CouponWizard"}
        response = requests.get(self.api_url, headers=headers)
        return response.json()

    def get_coupons(self):
        coupons = []
        response = self.get_response()

        for coupon in response:
            coupons.append(coupon["code"])

        return coupons
