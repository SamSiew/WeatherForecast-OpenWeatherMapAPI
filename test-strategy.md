# Test strategy

Author: Kenneth Huynh, Matti Haddad, Siew Ming Shern

Test cases in `test_openweather.py` are run automatically by CI server.

Please note some tests are for parsing category only, while others are for program functionality.

## Argument parsing and sanitization

Other than one specific case (refer to temp and time subsection), argument parsing and sanitization is 
done by [argprse library](https://docs.python.org/dev/library/argparse.html). the following are implemented by the library:

*  Api argument is set to `required` at every command
*  Locations are mutual exclusive and only one is `required` at every command
*  The number of parameters each takes is also handled by the api
*  The `help` functionality

This significantly decreased the number of test cases, as testing a library functionality is out of scope of the assignment. 
Instead of checking every combination of arguments only a couple of valid and invalid test cases and have been written for this section. These tests where chosen based on the specification and program behavior:

*  All arguments at once 
*  Maximum allowed valid args with `help`
*  Maximum allowed valid args without `help`
*  Mutual exclusive location arguments: only one of these is allowed at a time `-city, -cid, -gc, -z` 
    *  This case is only tested once since (`-city, -cid, -gc, -z`) are in a mutual exclusive group handled by the library

Refer to `test_parse_arguments` function in `test_openweather.py`

For unknown arguments cases (invalid arguments and parameters), these were tested in an ad-hoc manner.

Refer to `test_unknown_arguments_ for_parse_arguments` function in `test_openweather.py`

### Temp and time (specific case)

MCDC (Modified condition/decision coverage) was used to run tests for -temp and -time arguments.
Since at least one of these option is required to run the program

Only Three cases are enough to achieve 100% statement and branch coverage for this specific case:

*  When temp and time are not included      Output: False
*  When time only is included               Output: True
*  When temp only is included               Output: True

Refer to `test_temp_and_time_args` function in `test_openweather.py`

## Testing temperature arguments

This tests the functionality of the command when specifying a temperature unit. The payload is checked for any changes
that reflect the specified unit given. As there are two cases, where one can be "celsius" and the other "fahrenheit",
these are test accordingly.

Refer to `test_temp_args` function in `test_openweather.py`

## Updating the payload

The method checks if certain arguments were given and update the payload accordingly.

For statement coverage, all possible arguments must be given.
Whereas for branch coverage, there must also be a case that results in a false condition for each conditional statement
which occurs when certain arguments are not given or altered. The conditional statements where the location arguments
are mutually exclusive, will have to be tested separately.
Data Flow Coverage is achieved here by continuously verifying if each argument is updated to program and 
the Storage for all argument in program is expected to updated with new value given from argument from user.


Refer to `update_payload` function in `test_openweather.py`

## Weather API Requests

To increase branch coverage, we used mocking to simulate a request from the API server as we want to guarantee
that the request made is a success and failure. So, both true and false cases are taken care of.
Condition Coverage is achieved here by verifying if statement is behaving appropriately when status code received from 
API is 200 and below and less than 400.   

Refer to `test_weather_request` function in `test_openweather.py`

## Printing the output

To achieve maximal branch coverage, the conditional statements referring to arguments given must be tested for
both true and false cases. To assert the right outcome mocking was used again to check if a print was successful.
The contents of the print can vary due to the API information, so instead it was checked if the print was called when
multiple arguments are given. Whereas, the only predictable print that would remain constant would be if only the
`-city` argument was true so this was also tested while keeping the conditional statements checking arguments false.

Refer to `test_output` function in `test_openweather.py`

## CI

### Statement coverage

Statement coverage has been integrated into CI.

The report can be viewed via the the web terminal or by downloading the html artifacts and opening `index.html`

### Branch coverage

Branch coverage has been integrated into CI.

The report can be viewed via the the web terminal or by downloading the html artifacts and opening `index.html`

### Unit test
Unit test has been integrated into CI.

The report can be viewed via the the web terminal or by downloading the artifacts and opening `test.txt`
