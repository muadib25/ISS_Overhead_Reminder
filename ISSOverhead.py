import requests
from datetime import datetime
import smtplib
import time

# find your location's coordinates here: https://www.latlong.net/
# TODO 1. account for exceptions and illegal input.
MY_LAT = float(input("What is your latitude?: "))
MY_LONG = float(input("What is your longitude?: "))
SENDER_EMAIL = input("Enter your email address: ")
SENDER_PASSWORD = input("Enter your email password: ")
SMTP_SERVER = input("Enter your provider\\'s SMTP suffix, e.g.'smtp.gmail.com' for Gmail: ")
RECIPIENT_EMAIL = input("Enter the Reminder recipient's email: ")


# Your position is within +5 or -5 degrees of the ISS position.
def look_up():
    """Sends an email to the recipient when it is dark and the ISS is overhead"""

    # TODO 2. Check if ISS is near only if it is dark.
    def is_iss_near():
        """Returns True if the ISS is overhead"""
        if MY_LAT+5 >= iss_latitude >= MY_LAT-5 and MY_LONG+5 >= iss_longitude >= MY_LAT-5:
            return True

    def is_it_dark():
        """Returns True when it is nighttime"""
        # if time is not between sunrise and sunset,
        if time_now.hour >= sunset or time_now.hour <= sunrise:
            # it is dark
            return True
        else:
            return False

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    # If the ISS is close to my current position, and it is currently dark
    if is_iss_near() and is_it_dark():
        # Then email me to tell me to look up.
        with smtplib.SMTP(SMTP_SERVER) as connection:
            connection.starttls()
            connection.login(SENDER_EMAIL, SENDER_PASSWORD)
            connection.sendmail(
                from_addr=SENDER_EMAIL,
                to_addrs=RECIPIENT_EMAIL,
                msg=f"Subject:ISS is now overhead!\n\n"
                    f"Look up, ISS is out there passing the night sky!"
            )

    print(time_now)
    print(iss_latitude)
    print(iss_longitude)
    time.sleep(60)

    # Run the code every 60 seconds.
    look_up()


look_up()
