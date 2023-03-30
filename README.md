# CouponWizard

**CouponWizard** is a Python script that automates the process of redeeming active coupons on your [BlackDesert](https://www.naeu.playblackdesert.com) account. With CouponWizard, you can redeem available coupons quickly and easily without the hassle of manually logging in and redeeming them yourself.

## Installation

To use CouponWizard, follow these steps:

1. Clone the repository

```bash
git clone https://github.com/lucashnvarela/CouponWizard.git
```

2. Install the required dependencies

```powershell
pip install -r requirements.txt
```

3. Set up your user credentials by following the instructions in the next section

### Setting up the user credentials

Before running the script, you must fill out the `user_credentials.json` file with either your Steam or Pearl Abyss account credentials. You can do this by editing the file directly or by running `setup.py`, which will prompt you to enter your account information and update the `user_credentials.json file` for you.

```json
{
  "steam": { 
    "username": "your_steam_username", 
    "password": "your_steam_password", 
    "pp_pin": "your_steam_parental_protection_pin (optional)" 
  },
  "pearl_abyss": {
    "email": "your_pearl_abyss_email",
    "password": "your_pearl_abyss_password" 
  }
}
```

### Running the script

To use CouponWizard, run `main.py` by executing the following command:

```powershell
python main.py
```

CouponWizard checks for available coupons before logging in to your BlackDesert account. If there are no coupons available, the script will not log in and will stop the execution. However, if there are coupons available, the script will log in to your account and automatically redeem them for you.

**Note:** During the login process, you may need to complete additional authentication steps required by your account provider. If you fail to complete the required authentication, the script will not be able to log in to your account and redeem the coupons.

#### Log file

After the script redeems the coupons, a file named `log.json` will be updated to include the list of the coupons and their submission status. This file can be useful if you want to keep track of which coupons you have already redeemed or to see how the submission process went.

## Privacy

CouponWizard does not store or access your user credentials in any way during script execution. The script only uses your credentials for the purpose of logging in to your BlackDesert account and redeeming any available coupons. Additionally, CouponWizard does not collect any personal information about you or your account. These privacy measures help ensure the security and privacy of your BlackDesert account when using CouponWizard.
