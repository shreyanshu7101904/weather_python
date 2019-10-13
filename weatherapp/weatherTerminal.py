import click
from datetime import datetime
from termcolor import colored
from .weather import *
import sys


type_docs = "type should be Today or DayWise for DayWise number of days is required"
location_docs = "pincode location is required"
days_docs = "Number of days between 1-15"
@click.command()
@click.option('--location', help=location_docs)
@click.option('--date', default=datetime.now(), help='number of greetings')
@click.option('--day', default="Today", help=type_docs)
@click.option('--noofdays', type=int, help=days_docs)
def main(location, date, day, noofdays):
    if not location:
        raise LocationArgumentError
    weather_ob = WeatherReport(pin_code=location, type_=day, date_time=date)
    weather_ob.performOperation(days=noofdays)


if __name__ == '__main__':

    main()
