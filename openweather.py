"""
Author: Siew Ming Shern, Kenneth Huynh, Matti Haddad
Date Created: 25/09/19
Last Updated: 16/10/19

Requirements:

python openweather.py
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
-h; --help

Kenneth's api_token = 'ad3d090e749a388432e6eb595ca1c3c5'

Command line:
python openweather.py -city Melbourne -api ad3d090e749a388432e6eb595ca1c3c5 -temp celsius -time
python openweather.py -gc -37.840935 144.946457 -api ad3d090e749a388432e6eb595ca1c3c5 -temp celsius -time
"""

import sys
import argparse
import requests
import datetime
import json


class WeatherForecast:
    """
    Class for WeatherForecast program

    Raises:
        argparse.ArgumentError: when at least one of -temp or -time arguments is not provided
        requests.exceptions.ConnectionError: when weather API request is not successful
    """
    def __init__(self, argv):
        """
        class init method
        
        Args:
            argv (list): list of commandline arguments
        """
        self.argv = argv
        self.parser = argparse.ArgumentParser(
            description="Finds the weather of a certain location and additional information.", allow_abbrev=False)
        self.me_group = self.parser.add_mutually_exclusive_group(required=True)
        self.payload = {}
        self.payload.update({'units': 'metric'})
        self.temp_units = " celsius"
        self.wind_units = " metres/sec"
        self.args = None

    def main(self):
        """
        Main method which steps through each method in the the class
        """
        self.init_argument()
        self.parse_arguments()
        self.update_payload()
        self.output()

    def init_argument(self):
        """
        Specifies the accepted command line arguments and options for the program
        
        Precondition:
            must be the called first
        """
        self.parser.add_argument("-api", nargs=1, required=True,
                                 help="The API token associated to an account from OpenWeather.")

        self.me_group.add_argument("-city", nargs=1, help="The name of the city.")
        self.me_group.add_argument("-cid", nargs=1, help="The ID of the city.")
        self.me_group.add_argument("-gc", nargs=2, help="The geographic coordinates of the location: Lat Lon")
        self.me_group.add_argument("-z", nargs=2,
                                   help="The ZIP code of the city. Arguments are given in the following order: "
                                        "ZIP-code Country-code.")

        self.parser.add_argument("-temp", nargs='?', const='celsius', choices=['celsius', 'fahrenheit'],
                                 help="Changes temperature units with the following: celsius, fahrenheit.(the default "
                                      "unit is celsius)")

        self.parser.add_argument("-time", action='store_true', help="Adds the current time of the location.")
        self.parser.add_argument("-pressure", action='store_true', help="Adds pressure information.")
        self.parser.add_argument("-cloud", action='store_true', help="Adds cloud information.")
        self.parser.add_argument("-humidity", action='store_true', help="Adds humidity information.")
        self.parser.add_argument("-wind", action='store_true', help="Adds wind information.")
        self.parser.add_argument("-sunset", action='store_true', help="Adds sunset information.")
        self.parser.add_argument("-sunrise", action='store_true', help="Adds sunrise information.")

    def parse_arguments(self):
        """
        parses and sanitizes commandline input(done by the argparse library)

        Precondition:
            self.init_argument() must be called before this method
        """
        self.args = self.parser.parse_args(args=self.argv)

    def update_payload(self):
        """
        Updates a dictionary that will be used to call weather API
        
        Precondition:
            self.parse_arguments() must be called before this method

        Raises:
            argparse.ArgumentError: when at least one of -temp or -time arguments is not provided
        """
        # Infeasible case 
        if not (self.args.time or self.args.temp):
            raise argparse.ArgumentError("at least one argument is required: -time or -temp")

        if self.args.api:  # will probably remove this line
            self.payload.update({'appid': self.args.api[0]})
        if self.args.city:
            self.payload.update({'q': self.args.city[0]})
        if self.args.cid:
            self.payload.update({'id': self.args.cid})
        if self.args.gc:
            self.payload.update({'lat': self.args.gc[0], 'lon': self.args.gc[1]})
        if self.args.z:
            self.payload.update({'zip': self.args.z[0] + "," + self.args.z[1]})
        if self.args.temp == "fahrenheit":
            self.payload.update({'units': 'imperial'})
            self.temp_units = " fahrenheit"
            self.wind_units = " miles/hour"

    def output(self):
        """
        prints the output of the of calling weather API
        
        Precondition:
            self.update_payload() must be called before this method

        Raises:
            requests.exceptions.ConnectionError: when weather API request is not successful
        """
        # Set up API request URL and query
        weather_api = 'http://api.openweathermap.org/data/2.5/weather?'

        # Extract API information of the city
        r = requests.get(weather_api, self.payload)

        if 200 >= r.status_code < 400:
            r_dict = r.json()  # JSON file becomes a dictionary

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

            sunset = r_dict['sys']['sunset']    # Sunset time, unix, UTC
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
            output_statement = ''
            # if the location is in the middle of the ocean
            try:
                output_statement += r_dict['name'] + " - " + r_dict['sys']['country'] + ': '
            except KeyError:
                output_statement += "No known city-country in this location. "
                pass

            if self.args.time:
                output_statement += "The current time is " + str(utc_offset) + ", "
            if self.args.temp:
                output_statement += "The temperature ranges from " + str(temp_min) + "-" + str(
                    temp_max) + self.temp_units + ". The weather consists of " + description + "."
            if self.args.pressure:
                output_statement += " The atmospheric pressure is " + str(pressure) + " hPa."
            if self.args.cloud:
                output_statement += " The cloudiness is " + str(cloud) + "%."
            if self.args.humidity:
                output_statement += " The humidity is " + str(humidity) + "%."
            if self.args.wind:
                if wind_deg_boolean:
                    output_statement += " There is a wind speed of " + str(
                        wind_speed) + self.wind_units + " from " + str(wind_degree) + " degrees."
                else:
                    output_statement += " There is a wind speed of " + str(wind_speed) + self.wind_units + "."
            if self.args.sunrise:
                output_statement += " The time of sunrise occurs at " + str(sunrise_time) + "."
            if self.args.sunset:
                output_statement += " The time of sunset occurs at " + str(sunset_time) + "."

            print(output_statement)

        else:
            message = json.loads(r.text)['message']
            raise requests.exceptions.ConnectionError(message)


def main(argv):
    """
    initializes WeatherForecast class instance and calls its main method
    
    Args:
        argv ([type]): [description]
    """
    weather = WeatherForecast(argv[1:])     # first argument is the name of the program, so no need to include it
    weather.main()


if __name__ == '__main__':
    main(sys.argv)
