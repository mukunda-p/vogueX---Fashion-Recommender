import imp


import requests


class Config:
    def __init__(self):
        self.API_KEY = "2448a3bd09d0422f50b57b619355c4b8"


class WeatherAPI:
    def __init__(self) -> None:
        self.config = Config()

    def getCurrentWeather(self, latitude, longitude):
        url = "https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&exclude=hourly,daily&appid={API_KEY}".format(
            latitude=latitude, longitude=longitude, API_KEY=self.config.API_KEY
        )
        response = requests.request("GET", url, headers={}, data={})
        if response.status_code != 200:
            raise Exception(
                "Weather API failed : response code : {code}".format(
                    code=response.status_code
                )
            )
        jsonResponse = response.json()
        return response.json()
