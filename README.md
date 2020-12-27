# TheoryTestMonitorUK

Booked your Theory Test but want to find an earlier test date and want to be notified for it? Here's a UK Theory Test monitor built in Python using the Requests module.

**HOW TO RUN**

Before starting, please install all of the needed libraries.

```
pip install requests
pip install bs4
pip install discord_webhook
```

1. First, head over to `main.py` and fine the `profile` attribute in the `Monitor()` class. Simply input all of your credentials in this dictionary.

```
self.profile = {
    "firstAndMiddleName": "YOUR_FIRST_AND_MIDDLE_NAME",
    "lastName": "YOUR_LAST_NAME",
    "birthDay": "YOUR_BIRTH_DAY",
    "birthMonth": "YOUR_BIRTH_MONTH",
    "birthYear": "YOUR_BIRTH_YEAR",
    "licenseNumber": "YOUR_LICENSE_NUMBER"
}
```

2. You can also input your Discord Webhook if you have one in the `discordWebhook` attribute inside the class also.

```
self.discordWebhook = "YOUR_DISCORD_WEBHOOK"
```

3. Run the script:

```
py main.py
```

**INFO**

- The script will ask for how many threads you wish to run, an ideal thread count would just be 3.
- You can input the month numbers you want to monitor for in the `month` randomization function.
- The default monitoring delay is 3.5 seconds, you can modify this also in the `delay` attribute in the `Monitor()` class.
- Any questions, just contact me on Discord: DrizzySZN#0001

**Have fun & good luck!**
