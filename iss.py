#!/usr/bin/env python

__author__ = 'Paul Racisz + Ruben Espino'
import turtle
import requests
import time

earth = "map.gif"
iss_icon = "iss.gif"

public_api = 'http://api.open-notify.org'


def whos_in_space():
    """Makes a get request to retrieve the names
    of the names of astronauts in space
    and the aircraft they are on."""
    r = requests.get(public_api + '/astros.json')
    r.raise_for_status()
    return r.json()["people"]


def current_cords():
    """Makes a get request to retrieve latitude and longitude coords
    for the ISS."""
    r = requests.get(public_api + '/iss-now.json')
    r.raise_for_status()
    location = r.json()["iss_position"]
    latitude = float(location["latitude"])
    longitude = float(location["longitude"])
    return latitude, longitude


def world_map(latitude, longitude):
    """Creating a graphic screen of a world map image, and putting the
    ISS icon on it as well."""
    # make a new screen
    map_image = turtle.Screen()
    # sets the resolution for the window = to image.
    map_image.setup(720, 360)
    # sets the background to the earth image.
    map_image.bgpic(earth)
    # sets the coords of the world -x, -y,  x, y.
    map_image.setworldcoordinates(-180, -90, 180, 90)

    # adds the icon to registered usage of the screen.
    map_image.register_shape(iss_icon)
    space_station = turtle.Turtle()  # creating a turtle object.
    # adds the icon to the screen.
    space_station.shape(iss_icon)
    # sets the orientation of the turtle object so that it's facing north.
    space_station.setheading(90)
    # no drawing when moving.
    space_station.penup()
    # moves the turtle to an absolute position.
    space_station.goto(longitude, latitude)
    return map_image


def next_overhead_time(lat, lon):
    """ Find out the next time the ISS while be overhead the
    specificed latitude and longitude"""
    parameters = {"lat": lat, "lon": lon}
    r = requests.get(public_api + "/iss-pass.json", params=parameters)
    r.raise_for_status()
    overhead_time = r.json()["response"][1]["risetime"]
    return time.ctime(overhead_time)


def main():
    # Prints out where the astronauts are at from the whos_in_space() function.
    astros_dict = whos_in_space()
    print("Current astronauts in space: {}".format(len(astros_dict)))
    for astro in astros_dict:
        print("Astronaut: {} \nSpacecraft: {}\n".format(
            astro["name"], astro["craft"]))

    # Lat and Long being passed from current_cords to print out where the ISS is.
    latitude, longitude = current_cords()
    print("Current ISS coordinates: \nLatitude = {}\nLongitude = {} ".format(
        latitude, longitude))

    # create a display of ISS on world_map
    earth_map = None
    try:
        # try to show turtle.
        earth_map = world_map(latitude, longitude)
        # show the next time turtle will be over Indianapolis
        indy_lat = 39.768403
        indy_lon = -86.158068
        # makes a turtle object for the yellow dot.
        location = turtle.Turtle()
        location.penup()
        location.color("yellow")
        location.goto(indy_lon, indy_lat)
        # draws a dot shape
        location.dot()
        location.hideturtle()
        overhead_time_value = next_overhead_time(indy_lat, indy_lon)
        # Writes the text of the time ISS will be overhead.
        location.write(overhead_time_value, align="center",
                       font=("Arial", 14, "normal"))

    except RuntimeError as error:
        print("Error: Problem loading graphics: " + str(error))
    if earth_map is not None:
        # if earth_map loads, click the map to close.
        print("Click world map to exit.")
        earth_map.exitonclick()


if __name__ == '__main__':
    main()
