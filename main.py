import requests
from datetime import datetime
import smtplib
import time

# program sends an email notifier if it is dark and iss is overhead (+/- 5 deg)

MY_LAT = 33.952461
MY_LNG = -117.584801

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
    "tzid": "America/Los_Angeles"
}

password = "yoie xmvd ebsh juyd"
my_email = "pythontester93@gmail.com"
other_email = "pythontester2002@yahoo.com"

# get the current hour
now_hour = datetime.now().hour

# get the current coordinates of ISS, and find its difference from our location
response = requests.get("http://api.open-notify.org/iss-now.json")
response.raise_for_status()
longitude = float(response.json()["iss_position"]["longitude"])
latitude = float(response.json()["iss_position"]["latitude"])
lng_difference = abs(longitude - parameters["lng"])
lat_difference = abs(latitude - parameters["lat"])
# print(lat_difference)
# print(lng_difference)

# get the sunset hour of our location
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunset = response.json()["results"]["sunset"]
sunset_hour = int(sunset.split("T")[1].split(":")[0])

# send email if all conditions met, have it repeat continuously every 60 seconds as long as program is on
while True:
    time.sleep(60)
    if now_hour >= sunset_hour:
        if lng_difference <= 5 and lat_difference <= 5:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=other_email,
                    msg="Subject:Look Up! ISS Overhead\n\n"
                        "Hi there, just a quick note to let you know the International Space Station is passing overhead right now. Take a look up at the sky!"
                )



