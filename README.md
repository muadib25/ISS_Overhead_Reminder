# ISS_Overhead_Reminder
A program that sends the recipient an email-reminder whenever the I.S.S. is passing over the sky.

## ABOUT
The [International Space Station](https://en.wikipedia.org/wiki/International_Space_Station) is a modular space station (habitable artificial satellite) in low Earth orbit. It orbits our planet at an average speed of 28,000 kilometres per hour (17,000 mph), and completes 15.5 orbits per day (93 minutes per orbit). From the surface of the Earth the ISS can be seen at night during a clear sky as a fast-moving light, but when and where it is going to pass over is very difficult to determine. 

This little program can notify you (or a recipient of your choice) via email when the ISS will be passing over your area at night, by taking into account:

- your local time
- your position on the planet 
- the ISS's position

## REQUIREMENTS
The following python modules are required (see source code):
- Requests
- Daytime
- Smtplib
- Time

## USAGE
The program asks for the Latitude and Longitude at your present location. 
For that, you can use a map service such as this: https://www.latlong.net/ 

It then asks for your email address as well as your associated password. 
You may want to use a test email account, since typing your password like this could pose a security risk.

Ultimately the program prompts for the email address to receive the Reminder, which could be either your sender email or your primary email.

**DISCLAIMER:** I am not responsible for any loss or acquisition by third parties of data or sensitive information that may occur during the execution of the program. You are solely responsible for the data you input through the prompts of this program. The source code of this program is quite transparent in what happens upon execution of the program so no data is sent to others. Regardless, you are encouraged to take appropriate measures as far as data security is concerned and make use of test email accounts.



Enjoy stargazing!
