import requests
from datetime import datetime
import smtplib
import time

# find your location's coordinates here: https://www.latlong.net/
# Check for exceptions and illegal input.
try:
    MY_LAT = float(input("What is your latitude? (E.g. -35 or 59.32): "))
except ValueError:
    print("Not a valid number. Try again.\n")
    MY_LAT = float(input("What is your latitude? (E.g. -35 or 59.32): "))

try:
    MY_LONG = float(input("\nWhat is your longitude? (E.g. -23 or 18.06): "))
except ValueError:
    print("Not a valid number. Try again.\n")
    MY_LONG = float(input("What is your longitude? (E.g. -23 or 18.06): "))

print("\nYou will now be entering the email address to send the message from, along with the password.\n"
      "It is STRONGLY recommended that you use a test email address instead of your main address.\n")
time.sleep(2)
SENDER_EMAIL = input("Enter your email address: ")
SENDER_PASSWORD = input("Enter your email password: ")
SMTP_SERVER = input("Enter your provider\'s SMTP suffix, e.g.'smtp.gmail.com' for Gmail: ")
# Use same email if input is empty
RECIPIENT_EMAIL = input("Enter the email address for the Reminder to be sent to (leave empty if same): ")
if RECIPIENT_EMAIL == "":
    RECIPIENT_EMAIL = SENDER_EMAIL

# Send a test email to the user
print("\nI will now send a test email to verify if the details you provided are correct.")
with smtplib.SMTP(SMTP_SERVER) as test_connection:
    test_connection.starttls()
    test_connection.login(SENDER_EMAIL, SENDER_PASSWORD)
    test_connection.sendmail(
        from_addr=SENDER_EMAIL,
        to_addrs=RECIPIENT_EMAIL,
        msg=f"Subject:ISS Overhead test email!\n\n"
            f"Congratulations, \n\nYou have successfully configured the ISS Overhead Reminder!\n"
            f"Happy stargazing!\n"
    )


# Your position is within +5 or -5 degrees of the ISS position.
def look_up():
    """Sends an email to the recipient when it is dark and the ISS is overhead"""

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

    # Getting info about the ISS
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

    # Getting info about local sunrise-sunset times
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    # If it is currently dark,
    if is_it_dark():
        # And if the ISS is close to my current position,
        if is_iss_near():

            # Print also a message in the console.
            print(time_now.date(), ", ", time_now.hour, ":", time_now.minute)
            print("\nLook up, ISS is out there crossing the night sky!")
            # Then email me to tell me to look up.
            with smtplib.SMTP(SMTP_SERVER) as new_connection:
                new_connection.starttls()
                new_connection.login(SENDER_EMAIL, SENDER_PASSWORD)
                new_connection.sendmail(
                    from_addr=SENDER_EMAIL,
                    to_addrs=RECIPIENT_EMAIL,
                    msg=f"Subject:ISS is now overhead!\n\n"
                        f"Look up, ISS is out there crossing the night sky!"
                )
    print("\nThe app will now run in the background and notify you by email when "
          "the I.S.S. is about to cross the sky.\n"
          "You can now minimize the window.\n")

    # Run the code every 60 seconds.
    time.sleep(60)
    look_up()


# Proceed if test mail was received, else break
test_successful = input("Did you receive the test email? (Y/N): ").lower()
if test_successful == "y":
    look_up()
else:
    print("\nERROR: Failed to send test email. Re-run the application and check for correct email details.")
