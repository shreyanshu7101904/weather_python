from datetime import datetime
from config import *
import requests


class RequestError(Exception):
    """Response Error Exception"""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        print("Error in response, Response Code = ", self.status_code)
        print("Error Message json", self.message)


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


    def getGeoCoordinates(self):
        url = location_point + apiKey + \
            "&format=json&language=en-IN&postalKey={}%3AIN".format((self.pin_code))
        response = requests.get(url)
        print(response.json())
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

    def pretty_print(self, **kwargs):
        for key in kwargs:
            print(key, "\t", end="")
            for val, cnt in enumerate(kwargs[key]):
                print(val,"\t", end="" )
                if cnt == 5:
                    print("\n")
            print("\n")

    def getHourlyForecast(self):
        hourly = hourly_url + apiKey +\
            "&format=json&geocode={}%2C{}&language=en-IN&units=m".format(self.lat,self.lon)
        response = requests.get(hourly)
        print(hourly)
        if response.status_code == 200:
            data = response.json()["vt1hourlyForecast"]
            process_time = data["processTime"]
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
                precpitation=precpitation,
                precpitation_type=precpitation_type,
                uv_index=uv_index,
                wind_compass=wind_compass,
                wind_degrees=wind_degrees,
                wind_speed=wind_speed,
                phrase=phrase,
                feels_like=feels_like
            )
        else:
            raise RequestError(response.status_code, response.json())

        # print(response.json())
if __name__ == "__main__":
    ob = WeatherReport("560062","a" )
    print(str(ob))
    print(ob.getGeoCoordinates())
    ob.getHourlyForecast()



