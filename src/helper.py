from geopy.geocoders import Nominatim
from src import weather
from src import search
from weather import api as wapi
from search import api as sapi

### module to write helper functions for APIs
class PreferencesHelper:
    def givePreferences(userid):
        pass


class WeatherHelper:
    def __init__(self) -> None:
        self.geolocator = Nominatim(user_agent="Your_Name")
        self.weatherAPI = wapi.WeatherAPI()

    def giveLocation(self, userid, city=None):
        # if city is none query the profile from the database and see if there is a city.
        # if city is not given chill
        location = self.geolocator.geocode(city)
        return (location.longitude, location.latitude)

    def getWeather(self, city=None):
        coordinates = self.giveLocation(city)
        weather = self.weatherAPI.getCurrentWeather(
            coordinates.longitude, coordinates.latitude
        )
        return weather


class RecommendationHelper:
    def __init__(self) -> None:
        self.searchAPIObj = sapi.SearchImages()
        self.weatherHelper = WeatherHelper()

    def giveRecommendations(self, occasion=None, city=None):
        preferences = PreferencesHelper.givePreferences(occasion)
        query_keywords = []

        weather = self.weatherHelper.getWeather(city)
        for pref in preferences:
            query_keywords.append(pref["color"] + " " + pref["dress_type"])

        query_keywords.append(weather["temperature_type"])
        links = self.searchAPIObj.image_search(query_keywords)
        return links
