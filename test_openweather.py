"""
Author: Sam Siew, Kenneth Huynh, Matti Haddad
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
import os
import unittest
from unittest.mock import *
import argparse

import requests

from openweather import WeatherForecast


def block_print():
    sys.stdout = open(os.devnull, 'w')


class UnitTest(unittest.TestCase):

    def setUp(self):
        """
        Sets up a valid command with all valid arguments entered
        """
        self.input = WeatherForecast(
            ['-city=Melbourne', '-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-temp=celsius', '-time', '-pressure', '-cloud', '-humidity', '-wind', '-sunset', '-sunrise'])
        self.input.init_argument()
        self.input.args = argparse.Namespace(
            api=['ad3d090e749a388432e6eb595ca1c3c5'], cid=None, city=['Melbourne'], cloud=True, gc=None,
            humidity=True, pressure=True, sunrise=True, sunset=True, temp='celsius', time=True,
            wind=True, z=None
        )
        self.input.payload = {'units': 'metric', 'appid': 'ad3d090e749a388432e6eb595ca1c3c5', 'q': 'Melbourne'}
        self.argv = self.input.argv

    def test_parse_arguments(self):
        """
        This methods test the parsing of argparse library
        """
        command = WeatherForecast(['openweather.py'])
        command.init_argument()
        with self.assertRaises(BaseException):
            command.parse_arguments()

        # test the parsing of all args without help
        command = WeatherForecast(
            ['-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-city=Melbourne',
             '-cid=7839805',
             '-gc=-37.813061 144.944214',
             '-z=94040 us',
             '-time',
             '-temp=celsius',
             '-pressure',
             '-cloud',
             '-humidity',
             '-wind',
             '-sunset',
             '-sunrise'])
        command.init_argument()
        with self.assertRaises(BaseException):
            command.parse_arguments()

        # test maximum allowed args with help, please refer to functionality behavoir 
        command = WeatherForecast(
            ['-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-cid=7839805',
             '-time',
             '-temp=celsius',
             '-pressure',
             '-cloud',
             '-humidity',
             '-wind',
             '-sunset',
             '-sunrise',
             '-h'])
        command.init_argument()
        with self.assertRaises(BaseException):
            command.parse_arguments()

        # test maximum allowed args without help
        command = WeatherForecast(
            ['-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-cid=7839805',
             '-time',
             '-temp=celsius',
             '-pressure',
             '-cloud',
             '-humidity',
             '-wind',
             '-sunset',
             '-sunrise'])
        command.init_argument()
        self.assertIsNone(command.parse_arguments(),
                          "failed test maximum allowed args without help, all arguments should produce a valid output")

        # test location arguments conflict at least once (in this case, city and cid)
        # Mutual exclusive location arguments: only one of these is allowed at a time -city, -cid, -gc, -z
        command = WeatherForecast(
            ['-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-city=Melbourne',
             '-cid=7839805',
             '-time'])
        command.init_argument()
        with self.assertRaises(BaseException):
            command.parse_arguments()

    def test_unknown_arguments_for_parse_arguments(self):
        """
        Test for unknown arguments for parsing
        """
        # use -minutes instead of -time  and use -computercloud instead of -cloud
        command = WeatherForecast(
            ['-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-city=Melbourne',
             '-minute',
             '-temp=celsius',
             '-pressure',
             '-computercloud',
             '-humidity',
             '-wind',
             '-sunset',
             '-sunrise'])
        command.init_argument()
        with self.assertRaises(BaseException):
            command.parse_arguments()

        # Add a rondom word, in this case sydney
        command = WeatherForecast(
            ['-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-city=Melbourne',
             '-time',
             '-temp=celsius',
             '-pressure',
             '-cloud',
             '-humidity',
             '-wind',
             '-sunset',
             '-sunrise',
             'Sydeny'])
        command.init_argument()
        with self.assertRaises(BaseException):
            command.parse_arguments()

        # Add a rondom word, in this case sydney
        command = WeatherForecast(
            ['-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-city=Melbourne',
             '-time',
             '-temp=celsius',
             '-pressure',
             '-cloud',
             '-humidity',
             '-wind',
             '-sunset',
             '-sunrise=rain'])
        command.init_argument()
        with self.assertRaises(BaseException):
            command.parse_arguments()

        # Use a incomplete argument, -tim instead of temp
        command = WeatherForecast(
            ['-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-city=Melbourne',
             '-time',
             '-tem=celsius',
             '-pressure',
             '-cloud',
             '-humidity',
             '-wind',
             '-sunset',
             '-sunrise'])
        command.init_argument()
        with self.assertRaises(BaseException):
            command.parse_arguments()

        # Use a non specified temp parameter, kelvin
        command = WeatherForecast(
            ['-api=ad3d090e749a388432e6eb595ca1c3c5',
             '-city=Melbourne',
             '-time',
             '-temp=kelvin',
             '-pressure',
             '-cloud',
             '-humidity',
             '-wind',
             '-sunset',
             '-sunrise'])
        command.init_argument()
        with self.assertRaises(BaseException):
            command.parse_arguments()

    def test_update_payload(self):
        """
        Tests if arguments given have updated the payload appropriately
        """
        # Test payload with only api and city
        command = WeatherForecast(['-city=Melbourne', '-api=ad3d090e749a388432e6eb595ca1c3c5'])
        command.init_argument()
        command.parse_arguments()
        with self.assertRaises(BaseException):
            command.update_payload()

        # Test payload with only city
        command = WeatherForecast(['-city=Melbourne'])
        command.init_argument()
        command.args = argparse.Namespace(
            api=None, cid=None, city=['Melbourne'], cloud=False, gc=None,
            humidity=False, pressure=False, sunrise=False, sunset=False, temp=None, time=False, wind=False, z=None
        )
        with self.assertRaises(BaseException):
            command.update_payload()

        # Payload is updated for all arguments except gc and z and city
        command = WeatherForecast([
            '-api=ad3d090e749a388432e6eb595ca1c3c5',
            '-cid=7839805',
            '-time',
            '-temp=celsius',
            '-pressure',
            '-cloud',
            '-humidity',
            '-wind',
            '-sunset',
            '-sunrise'
        ])
        command.init_argument()
        command.args = argparse.Namespace(
            api=['ad3d090e749a388432e6eb595ca1c3c5'], cid=['7839805'], city=None, cloud=True,
            gc=None, humidity=True, pressure=True, sunrise=True, sunset=True,
            temp='celsius', time=True, wind=True, z=None
        )
        command.update_payload()
        self.assertEqual(command.payload,
                         {'units': 'metric', 'appid': 'ad3d090e749a388432e6eb595ca1c3c5', 'id': ['7839805']})

        # Payload is updated with gc
        command = WeatherForecast([
            '-api=ad3d090e749a388432e6eb595ca1c3c5',
            '-gc=-37.8139992 144.9633179',
            '-time',
            '-temp=celsius',
        ])
        command.init_argument()
        command.args = argparse.Namespace(
            api=['ad3d090e749a388432e6eb595ca1c3c5'], cid=None, city=None, cloud=False, gc=['-37.840935', '144.946457'],
            humidity=False, pressure=False, sunrise=False, sunset=False, temp='celsius', time=False, wind=False, z=None
        )
        # Test payload has updated
        command.update_payload()
        self.assertEqual(command.payload,
                         {
                             'units': 'metric',
                             'appid': 'ad3d090e749a388432e6eb595ca1c3c5',
                             'lat': '-37.840935',
                             'lon': '144.946457'
                         })

        # Payload is updated z
        command = WeatherForecast([
            '-api=ad3d090e749a388432e6eb595ca1c3c5',
            '-z=94040 us',
            '-time',
            '-temp=celsius',
        ])
        command.init_argument()
        command.args = argparse.Namespace(
            api=['ad3d090e749a388432e6eb595ca1c3c5'], cid=None, city=None, cloud=False,
            gc=None, humidity=False, pressure=False, sunrise=False, sunset=False,
            temp='celsius', time=True, wind=False, z=['94040', 'us']
        )
        command.update_payload()
        self.assertEqual(command.payload,
                         {'units': 'metric', 'appid': 'ad3d090e749a388432e6eb595ca1c3c5', 'zip': '94040,us'})

    def test_if_no_temp_or_time(self):
        """
        tests for -temp and -time arguments, using MCDC (Modified condition/decision coverage))
        This method is about Parsing and sanitization only

        Only Three cases
        *  when temp and time are not included      Output: False
        *  when time only is included               Output: True
        *  when temp only is included               Output: True

        """
        # Both temp and time not included
        command = WeatherForecast(
            ['-city=Melbourne', '-api=ad3d090e749a388432e6eb595ca1c3c5']
        )
        command.init_argument()
        command.parse_arguments()
        with self.assertRaises(BaseException):
            command.update_payload()

        # Only temp is included with fahrenheit as argument
        command = WeatherForecast(
            ['-city=Melbourne', '-api=ad3d090e749a388432e6eb595ca1c3c5', '-temp=fahrenheit']
        )
        command.init_argument()
        command.parse_arguments()
        self.assertIsNone(command.update_payload(), "the output should be valid temp fahrenheit functionality")

        # Only time is included
        command = WeatherForecast(
            ['-city=Melbourne', '-api=ad3d090e749a388432e6eb595ca1c3c5', '-time']
        )
        command.init_argument()
        command.parse_arguments()
        self.assertIsNone(command.update_payload(), "the output should be valid with a time argument")

    def test_temp_args(self):
        """
        Tests the functionality of possible parameters for the celsius argument.
        """
        # Only temp is included with no argument
        command = WeatherForecast(
            ['-city=Melbourne', '-api=ad3d090e749a388432e6eb595ca1c3c5', '-temp']
        )
        command.init_argument()
        command.parse_arguments()
        self.assertIsNone(command.update_payload(), "the output should be valid with temp celsius functionality")

        # Only temp is included with celsius as argument
        command = WeatherForecast(
            ['-city=Melbourne', '-api=ad3d090e749a388432e6eb595ca1c3c5', '-temp=celsius']
        )
        command.init_argument()
        command.parse_arguments()
        self.assertIsNone(command.update_payload(), "the output should be valid with temp celsius functionality")

    def test_output(self):
        """
        Tests the functionality of the output function. Checks if it will print out an appropriate output.
        """
        # Test with all viable arguments
        with patch('openweather.print') as mock_print:
            request_success = self.input.output()
            self.assertIsNone(request_success)
            mock_print.assert_called_once()

        # Test with no viable arguments for the conditional statements
        with patch('openweather.print') as mock_print:
            self.input.args = argparse.Namespace(
                api=['ad3d090e749a388432e6eb595ca1c3c5'], cid=None, city=['Melbourne'], cloud=False, gc=None,
                humidity=False, pressure=False, sunrise=False, sunset=False, temp='', time=False,
                wind=False, z=None
            )
            request_success = self.input.output()
            self.assertIsNone(request_success)
            mock_print.assert_called_once_with('Melbourne - AU: ')

        # Test with edge case where geo coordinate is not of a specific city
        with patch('openweather.print') as mock_print:
            self.input.args = argparse.Namespace(
                api=['ad3d090e749a388432e6eb595ca1c3c5'], cid=None, city=None, cloud=False,
                gc=['37.840935', '144.946457'], humidity=False, pressure=False, sunrise=False,
                sunset=False, temp='celsius', time=False, wind=False, z=None
            )
            self.input.payload = {
                             'units': 'metric',
                             'appid': 'ad3d090e749a388432e6eb595ca1c3c5',
                             'lat': '37.840935',
                             'lon': '144.946457'
                         }
            request_success = self.input.output()
            self.assertIsNone(request_success)
            mock_print.assert_called_once()

    def test_weather_request(self):
        """
        Simulates a request to the Weather API server for both successful and unsuccessful.
        """
        with patch('openweather.requests.get') as mocked_get:
            # Code to test a successful API request connection
            with patch('openweather.datetime.timedelta') as mocked_datetime:
                mocked_get.return_value.status_code = 200
                mocked_datetime.attribute.seconds = 39600
                request_success = self.input.output()
                mocked_get.assert_called_with('http://api.openweathermap.org/data/2.5/weather?', self.input.payload)
                self.assertIsNone(request_success)

            # Code to test a failed API request connection
            with patch('openweather.json.loads') as mocked_dict:
                mocked_dict.attribute['message'] = 'Bad response'
                mocked_get.return_value.status_code = 400
                with self.assertRaises(requests.exceptions.ConnectionError):
                    self.input.output()


if __name__ == '__main__':
    block_print()
    unittest.main()
