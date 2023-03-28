# CouponWizard

**CouponWizard** is a Python script that automates the process of redeeming active coupons on your [BlackDesert](https://www.naeu.playblackdesert.com) account. With CouponWizard, you can redeem available coupons quickly and easily without the hassle of manually logging in and redeeming them yourself.

## Usage

### Using Steam account

To use the script with your Steam account, simply run `main.py` with the following command line arguments:

```powershell
python main.py --steam_username <username> --steam_password <password> [--steam_pp_pin <pin>]
```

- `--steam_username`: Your Steam account username
- `--steam_password`: Your Steam password
- `--steam_pp_pin`: Your Steam parental protection pin <sup>optional</sup>

### Using Pear Abyss account

To use the script with your Pearl Abyss account, simply run `main.py` with the following command line arguments:

```powershell
python main.py --pa_email <email> --pa_password <password>
```

- `--pa_email`: Your Pearl Abyss account email
- `--pa_password`: Your Pearl Abyss account password

The script will log in to your account and automatically attempt to redeem any available coupons. If there are no coupons available, the script will simply exit.

**Note:** During the login process, you may need to complete additional authentication steps required by your account provider. If you fail to complete the required authentication, the script will not be able to log in to your account and redeem the coupons.

## Privacy

To ensure your privacy, CouponWizard does not store your user credentials. The credentials are only used for authentication with your account provider and are not accessed or saved during script execution.

## Dependencies

CouponWizard requires the following Python packages:

- `requests`
- `selenium`

You can install these dependencies by running the following command:

```powershell
pip install -r requirements.txt
```
