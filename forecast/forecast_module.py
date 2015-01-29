__author__ = 'patinbsb'

# Imports

import urllib
from json import loads
import time

# Using previous code to get local weather info


def grab_weather():

    lat = 45.5
    lng = -0.6

    # Getting the weather info and converting json to a dictionary object
    while True:

        try:
            weather = urllib.urlopen(
                "http://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}".format(lat, lng)).read()
        except:
            time.sleep(5)
            continue

        try:
            wdata = loads(weather)
            break
        except:
            time.sleep(5)
            continue

    return wdata


def weather_iter(block, wdata):

    NE, SE, SW, NW = (range(22, 67), range(112, 157), range(202, 247), range(292, 337))
    E, S, W = (range(67, 112), range(157, 202), range(247, 292))
    N = [(337, 360), (0, 22)]

    # getting all the relevant info from the json object
    try:
        status = (wdata["list"][block]["weather"][0]["main"])
    except:
        status = "unknown"
        pass

    try:
        descrip = (wdata["list"][block]["weather"][0]["description"])
    except:
        descrip = "unknown"
        pass

    try:
        temp = (str(int(float(wdata["list"][block]["main"]["temp"]) - 273.15))) + " Degrees C"
    except:
        temp = "unknown"
        pass

    try:
        windspeed = int((wdata["list"][block]["wind"]["speed"]) * 2.23)
    except:
        wind = "unknown"
        pass

    forces = [(0, 1), (1, 3), (4, 7), (8, 12), (13, 18), (19, 24), (25, 31), (32, 38), (39, 46), (47, 54), (55, 63),
              (64, 75)]
    force_count = 0

    # Formatting
    for force in forces:
        if windspeed in range(force[0], force[1] + 1):
            wind = str(force_count)
        force_count += 1

    try:
        deg = (int(wdata["list"][block]["wind"]["deg"]))

        if deg in NE:
            winddir = "North East"
        if deg in SE:
            winddir = "South East"
        if deg in SW:
            winddir = "South West"
        if deg in NW:
            winddir = "North West"
        if any(lower <= deg <= upper for (lower, upper) in N):
            winddir = "North"
        if deg in E:
            winddir = "East"
        if deg in S:
            winddir = "South"
        if deg in W:
            winddir = "West"
    except:
        winddir = "unknown"
        pass

    try:
        rain = (str(wdata["list"][block]["rain"]["3h"])) + " mm"
    except:
        rain = "unknown"
        pass

    try:
        temphigh = (str(int(float(wdata["list"][block]["main"]["temp_max"]) - 273.15))) + " Degrees C"
    except:
        temphigh = "unknown"
        pass

    try:
        region = (wdata["city"]["name"])
    except:
        region = "unknown"

    return temp, descrip, wind, winddir


if __name__ == "__main__":
    grab_weather()