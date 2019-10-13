from datetime import datetime
from config import *
import requests
from termcolor import colored


class RequestError(Exception):
    """Response Error Exception"""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        print(colored("Error in response, Response Code = ", 'red'), colored(self.status_code, 'yellow'))
        print("Error Message json", self.message)

class NumberOfDaysError(Exception):
    def __init__(self, days):
        self.days = days
        print(colored("Number of days is between 1-15", 'Red'), colored(self.days, 'yellow'))



class WeatherReport:

    def __init__(self, pin_code, type_, date_time=None, lat=None, lon=None):
        self.pin_code = pin_code
        self.type = type_
        if date_time:
            self.date_time = date_time
        else:
            self.date_time = datetime.now()
        self.lat = None
        self.lon = None
        self.place_id = None


    def __str__(self):
        return str(self.pin_code)

    def _convertDatetimeToStr(self, values):

        return [str(datetime.strptime(i.split("+")[0], \
                '%Y-%m-%dT%H:%M:%S'))for i in values if i is not '']

    def getGeoCoordinates(self):
        url = location_point + apiKey + \
            "&format=json&language=en-IN&postalKey={}%3AIN".format((self.pin_code))
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.lon = data["location"]["longitude"]
            self.lat = data["location"]["latitude"]
            city = data["location"]["city"]
            local = data["location"]["locale"]
            place = " ".join([local[i].strip() for i in local if local[i]])
            self.place_id = data["location"]["placeId"]
            return city, place
        else:
            raise RequestError(response.status_code, response.json())

    def pretty_print(self, days=None, **kwargs):
        for key in kwargs:
            print(colored(key, 'green'), "\t", end="")
            for cnt, val in enumerate(kwargs[key]):
                print(colored(val, 'yellow'), "\t", end="" )
                if cnt == 5:
                    print("\n")
            print("\n")

    def getHourlyForecast(self):
        hourly = hourly_url + apiKey +\
            "&format=json&geocode={}%2C{}&language=en-IN&units=m".format(self.lat,self.lon)
        response = requests.get(hourly)
        if response.status_code == 200:
            data = response.json()["vt1hourlyForecast"]
            process_time = self._convertDatetimeToStr(data["processTime"])
            temperature = data["temperature"]
            precpitation = data["precipPct"]
            precpitation_type = data["precipType"]
            uv_index = data["uvIndex"]
            wind_compass = data["windDirCompass"]
            wind_degrees = data["windDirDegrees"]
            wind_speed = data["windSpeed"]
            phrase = data["phrase"]
            feels_like = data["feelsLike"]
            self.pretty_print(
                Time=process_time,
                Temperature = temperature,
                Phrase=phrase,
                Feels_Like=feels_like,
                Precpitation=precpitation,
                PrecpitationType=precpitation_type,
                UV_Index=uv_index,
                Wind_Compass=wind_compass,
                Wind_Degrees=wind_degrees,
                Wind_Speed=wind_speed
            )
        else:
            raise RequestError(response.status_code, response.json())

    def getDayWiseForecast(self, days):
        if days < 0 or days > 15:
            raise NumberOfDaysError(days)
        daily_forecast = daily_url + apiKey +\
        "&format=json&geocode={}%2C{}&language=en-IN&units=m".format(self.lat,self.lon)
        response = requests.get(daily_forecast)
        if response.status_code == 200:
            data = response.json()["vt1dailyForecast"]
            dates = self._convertDatetimeToStr(data["validDate"])
            sunrise = self._convertDatetimeToStr(data["sunrise"])
            sunset = self._convertDatetimeToStr(data["sunset"])
            moon_phrase = data["moonPhrase"]
            moonrise = self._convertDatetimeToStr(data["moonrise"])
            moonset = self._convertDatetimeToStr(data["moonset"])
            day_of_week = data["dayOfWeek"]
            precipitation = data["day"]["precipPct"]
            precipitation_amount = data["day"]["precipAmt"]
            temprature = data["day"]["temperature"]
            uvindex = data["day"]["uvIndex"]
            uv_description = data["day"]["uvDescription"]
            phrase = data["day"]["phrase"]
            narrative = data["day"]["narrative"]
            humidity = data["day"]["humidityPct"]
            wind_speed = data["day"]["humidityPct"]
            winddirdegrees = data["day"]["windDirDegrees"]
            self.pretty_print(
                Date = dates,
                Sunrise = sunrise,
                Sunset = sunset,
                Moon_Phrase = moon_phrase,
                Moon_Rise = moonrise,
                Moon_Set = moonset,
                Temprature = temprature,
                Narrative = narrative,
                Day_Of_Week = day_of_week,
                Precipitation = precipitation,
                Precipitation_Amount = precipitation_amount,
                UV_Index = uvindex,
                UV_Description = uv_description,
                Phrase = phrase,
                Humidity = humidity,
                Wind_Speed = wind_speed,
                Wind_Direction = winddirdegrees
                )
            pass
        else:
            raise RequestError(response.status_code, response.json())


if __name__ == "__main__":
    ob = WeatherReport("560062","a" )
    print(str(ob))
    print(ob.getGeoCoordinates())
    # ob.getHourlyForecast()
    ob.getDayWiseForecast(5)
    





