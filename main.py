from utils.CouponRequester import CouponRequester


def main():
    with CouponRequester() as requester:
        print(requester.get_coupons())


if __name__ == "__main__":
    main()
