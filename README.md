# Project: Weatherforecast

A command-line program in Python 3+ to get weather forecast through the OpenWeatherMap API

## Repository information

FIT2107 project repository for assignment 3 white box testing

**Team: MattiKen**

**Members: KH MH MS**

Each member works on his own branch and submits a merge request when needed, CI must pass before merging

### CI:
Runs three stages:

*  Statement coverage
*  Branch coverage
*  run tests

The CI output is in the [CI/DC section](https://git.infotech.monash.edu/fit2107-s2-2019/MattiKen/project/pipelines).

Each stage produces a report, These reports can be viewed via the the web terminal or by downloading the html artifacts and opening `index.html`

### Style Guide for Python Code
Use PEP-8


### Python libraries and api used:
*  sys
*  argparse
*  requests
*  datetime
*  json
*  OpenWeatherMap API

### Running Environment 

The program is meant for Linux based operating systems. Run on Windows at your own risk.

## Instruction

openweather.py accepts the following arguments 

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

Please Note the program doesn't use `=`, rather it uses a space to separate argument from parameters

Ex: `python openweather.py -city Melbourne -api xxxxx -temp celsius`

if the argument requires 2 parameters then separate them with a space,

Ex: `python openweather.py -gc -37.840935 144.946457 -api xxxxx -temp celsius`

## Program functionality behavior 

Refer to this [forum post](https://lms.monash.edu/mod/forum/discuss.php?d=1753417) for the first 2 points 

Please Note that you need to provide your own weather API key in all examples

*  In case duplicates arguments are used, then the parser simply accept the last one only (same as Linux utilities)

    Ex: `python openweather.py -city Sydney -city Geelong -city Melbourne -api xxxxx -temp celsius`

    Output: The program will accepts the last one only(Melbourne), that is, it will show the output of requesting Melbourne city

*  In case `-h` or `--help` is one of the arguments when executing the program( where by if `-h` or `--help` is removed the program produces a valid output), then the program will ignore everything and only show `--help` functionality (same as Linux utilities)

    Ex: `python openweather.py -city Melbourne -api xxxxx -temp celsius --help`

    Output: The program will show help only functionality only 

*  In case of Invalid arguments parsing it will always print the program usage followed by the error, please note this is **not** the `help` functionality.

    Ex: `python openweather.py -city Melbourne -api xxxxx -temp celsius -minute`

        usage: openweather.py [-h] -api API
            (-city CITY | -cid CID | -gc GC GC | -z Z Z)
            [-temp [{celsius,fahrenheit}]] [-time] [-pressure]
            [-cloud] [-humidity] [-wind] [-sunset] [-sunrise]
        openweather.py: error: unrecognized arguments: -minute

*  The order of program arguments does not matter(same as Linux utilities)

    Ex: `python openweather.py -city Melbourne -api xxxxx -tem celsius`
    
    is the same as 

    Ex: `python openweather.py -api xxxxx -tem celsius -city Melbourne`

*  Main Errors raised by the program are not handled this is beacause of the specification on page 5:

        Please note that you are not required to deal
        with exception handling in this assignment).

    Two errors are handled in the output method, this is because the information returned by the API were still considered valuabe for the user.
    
Where xxxxx is the weather API token

Please note on **Linux**, `pyhton3` instead of `python` might be needed to run the program.

## Other


### Run code coverage locally 

In case you want to run coverage locally on command line 

**LINUX**

    TO RUN STATEMENT COVERAGE
        coverage run test_openweather.py; coverage report -m; coverage html -d statement_coverage

    TO RUN BRANCH COVERAGE 
        coverage run --branch test_openweather.py; coverage report -m; coverage html -d branch_coverage

    TO OPEN HTML REPORTS (replace "firefox" with your browser name)
        cd statement_coverage/htmlcov; firefox index.html
        cd branch_coverage/htmlcov; firefox index.html

**WINDOWS**

    TO RUN
        coverage run test_openweather.py & coverage report -m & coverage html -d statement_coverage

    TO RUN BRANCH COVERAGE
        coverage run --branch test_openweather.py & coverage report -m & coverage html -d branch_coverage

    TO OPEN HTML REPORTS
        cd statement_coverage/htmlcov & index.html
        cd branch_coverage/htmlcov & index.html

