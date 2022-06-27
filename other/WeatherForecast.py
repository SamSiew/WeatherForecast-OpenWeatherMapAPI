"""
Date Created: 25/09/19
Last Updated: 25/09/19

Requirements:

python myopenweather.py
-api = API token
-city = city name
-cid = city id
-gc = geographic coordinates
-z = zip code
-time
-temp = (celsius, fahrenheit) (the default unit is celsius)
-pressure
-cloud
-humidity
-wind
-sunset
-sunrise
-help

Kenneth's api_token = 'ad3d090e749a388432e6eb595ca1c3c5'

Command line: python WeatherForecast.py -city Melbourne -api ad3d090e749a388432e6eb595ca1c3c5 -temp celsius -time
"""

import sys
import argparse
import requests
import datetime


def main(argv):
    parser = argparse.ArgumentParser(description="Finds the weather of a certain location and additional information.")
    me_group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("-api", nargs=1, required=True, help="The API token associated to an account from OpenWeather.")

    # parser.add_argument("-city", nargs=1,  help="The name of the city.")
    # parser.add_argument("-cid", nargs=1,  help="The ID of the city.")
    # parser.add_argument("-gc", nargs=2, help="The geographic coordinates of the location.")
    # parser.add_argument("-z", nargs=2,
    #                     help="The ZIP code of the city. Arguments are given in the following order: ZIP code, "
    #                          "country code.")
    me_group.add_argument("-city", nargs=1, help="The name of the city.")
    me_group.add_argument("-cid", nargs=1, help="The ID of the city.")
    me_group.add_argument("-gc", nargs=2, help="The geographic coordinates of the location: Lat Lon")
    me_group.add_argument("-z", nargs=2,
                          help="The ZIP code of the city. Arguments are given in the following order: ZIP-code  "
                               "Country-code.")

    parser.add_argument("-temp", nargs=1, choices=['celsius', 'fahrenheit'],
                        help="Changes temperature units with the following: celsius, fahrenheit.")

    parser.add_argument("-time", action='store_true', help="Adds the current time of the location.")
    parser.add_argument("-pressure", action='store_true', help="Adds pressure information.")
    parser.add_argument("-cloud", action='store_true', help="Adds cloud information.")
    parser.add_argument("-humidity", action='store_true', help="Adds humidity information.")
    parser.add_argument("-wind", action='store_true', help="Adds wind information.")
    parser.add_argument("-sunset", action='store_true', help="Adds sunset information.")
    parser.add_argument("-sunrise", action='store_true', help="Adds sunrise information.")
    # parser.add_argument("-help", action='store_true', help="Outputs user help documentation for the program.")

    if len(argv) <= 1:
        parser.print_help()
        raise ValueError("There were no arguments specified.")

    args, unknown = parser.parse_known_args(args=argv)

    # if len(args.city) > 1:
    #     parser.error("Duplicated city arguments, only one is allowed. ")

    # duplicated case
    # print(len(args.city), args.city)

    # print("Arguments:", args, "\n")     # TODO: REMOVE

    payload = {}
    temp_units = " celsius"
    wind_units = " metres/sec"

    # TODO: Fix test case
    """
    # Check for multiple location arguments
    location_args = len(args.city) + len(args.cid) + len(args.gc) + len(args.z)
    if location_args > 1:
        raise argparse.ArgumentError("Cannot have more than one location argument specified.")
    """

    if args.api:  # will probably remove this line
        payload.update({'appid': args.api[0]})
    if args.city:
        payload.update({'q': args.city[0]})
    if args.cid:
        payload.update({'id': args.cid})
    if args.gc:
        payload.update({'lat': args.gc[0], 'lon': args.gc[1]})
    if args.z:
        payload.update({'zip': args.z[0] + "," + args.z[1]})
    if args.time:
        pass
    if args.temp:
        if args.temp[0] == "celsius":
            payload.update({'units': 'metric'})
        elif args.temp[0] == "fahrenheit":
            payload.update({'units': 'imperial'})
            temp_units = " fahrenheit"
            wind_units = " miles/hour"

    # Infeasible case 2.
    if not (args.time or args.temp):
        raise argparse.ArgumentError("at least one argument is required: -time or -temp")

    # if args.pressure:
    #     pass
    # if args.cloud:
    #     pass
    # if args.humidity:
    #     pass
    # if args.wind:
    #     pass
    # if args.sunset:
    #     pass
    # if args.sunrise:
    #     pass
    # elif args.help:
    #     parser.print_help()
    #     exit(1)

    # Infeasible case 2
    # if not (args.api or args.city or args.cid or args.gc or args.z or args.time or args.temp) and args.help:
    #     parser.print_help()
    #     exit(1)
    # else:
    #     raise argparse.ArgumentError("Program can't show help with other commands, please use help as the only argument.")

    # Set up API request URL and query
    weather_api = 'http://api.openweathermap.org/data/2.5/weather?'

    # print("payload:", payload, "\n")  # TODO: REMOVE

    # Extract API information of the city
    r = requests.get(weather_api, payload)
    if 200 >= r.status_code < 400:
        r_dict = r.json()  # JSON file becomes a dictionary

        # Print JSON contents TODO: REMOVE
        print("JSON information:")
        for x in r_dict:
            print("%s: %s" % (x, r_dict[x]))
        print()

        # Assign data
        description = r_dict['weather'][0]['description']
        city_timezone_offset = r_dict['timezone']  # Offset in seconds from UTC

        temp_min = r_dict['main']['temp_min']
        temp_max = r_dict['main']['temp_max']

        pressure = r_dict['main']['pressure']
        cloud = r_dict['clouds']['all']
        humidity = r_dict['main']['humidity']

        wind_speed = r_dict['wind']['speed']
        try:
            wind_degree = r_dict['wind']['deg']
            wind_deg_boolean = True
        except KeyError:
            wind_deg_boolean = False

        sunset = r_dict['sys']['sunset']  # Sunset time, unix, UTC
        sunrise = r_dict['sys']['sunrise']  # Sunrise time, unix, UTC

        # Calculate time in human-readable format
        utc = datetime.datetime.utcnow()
        utc_offset = utc + datetime.timedelta(seconds=city_timezone_offset)
        utc_offset = utc_offset.strftime("%d-%m-%Y %I:%M %p")

        # Calculate the sunset time in a human-readable format
        sunset_time = datetime.datetime.fromtimestamp(sunset)
        sunset_time = sunset_time.strftime("%d-%m-%Y %I:%M %p")

        # Calculate the sunrise time in a human-readable format
        sunrise_time = datetime.datetime.fromtimestamp(sunrise)
        sunrise_time = sunrise_time.strftime("%d-%m-%Y %I:%M %p")

        # Builds the output statement
        output_statement = r_dict['name'] + " - " + r_dict['sys']['country'] + ': '
        if args.time:
            output_statement += "The current time is " + str(utc_offset) + ", "
        if args.temp:
            output_statement += "The temperature ranges from " + str(temp_min) + "-" + str(temp_max) + temp_units \
                                + ". The weather consists of " + description + "."
        if args.pressure:
            output_statement += " The atmospheric pressure is " + str(pressure) + " hPa."
        if args.cloud:
            output_statement += " The cloudiness is " + str(cloud) + "%."
        if args.humidity:
            output_statement += " The humidity is " + str(humidity) + "%."
        if args.wind:
            if wind_deg_boolean:
                output_statement += " There is a wind speed of " + str(wind_speed) + wind_units + " from " \
                                    + str(wind_degree) + " degrees."
            else:
                output_statement += " There is a wind speed of " + str(wind_speed) + wind_units + "."
        if args.sunrise:
            output_statement += " The time of sunrise occurs at " + str(sunrise_time) + "."
        if args.sunset:
            output_statement += " The time of sunset occurs at " + str(sunset_time) + "."

        print(output_statement)

    else:
        print(r.text)  # TODO print message only
        exit(1)
        raise requests.exceptions.ConnectionError("Could not forward request.")


if __name__ == '__main__':
    main(sys.argv)
