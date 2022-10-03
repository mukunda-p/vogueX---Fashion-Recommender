import imp


import requests

class Config:
    def __init__(self):
        self.API_KEY = "9a00260af2814c1b8c1182732220310"


class WeatherAPI:
    def __init__(self) -> None:
        self.config = Config()

    def getCurrentWeather(self, latitude=None, longitude=None, city = None):
        url = "http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no".format(city=city, API_KEY=self.config.API_KEY)
        response = requests.request("GET", url, headers={}, data={})
        if response.status_code != 200:
            raise Exception("Weather API failed : response code : {code}".format(code = response.status_code))
        jsonResponse = response.json()
        if 'condition' in jsonResponse:
            return jsonResponse['condition']['text']
        return ''

    

