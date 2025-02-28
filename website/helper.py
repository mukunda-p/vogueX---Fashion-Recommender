# from geopy.geocoders import Nominatim

import json

from . import models
from . import utils

default_preferences = {
    "male": ["blue shirt", "black pant"],
    "female": ["blue shirt", "black pant"],
}


# module to write helper functions for APIs


class PreferencesHelper:
    def givePreferences(userid, occasion):
        try:
            preferenceObj = models.Preference.query.filter_by(
                userid=userid).first()
            preferences = json.loads(str(preferenceObj.preferences))
            if occasion in preferences:
                return preferences[occasion]
        except:
            return None


class WeatherHelper:
    def __init__(self) -> None:
        # self.geolocator = Nominatim(user_agent="Your_Name")
        self.weatherAPI = utils.WeatherAPI()

    # def giveLocation(self, userid, city = None):
    #     # if city is none query the profile from the database and see if there is a city.
    #     # if city is not given chill
    #     location = self.geolocator.geocode(city)
    #     return (location.longitude, location.latitude)

    def getWeather(self, city=None, date=None, time=None):
        # coordinates = self.giveLocation(city)
        # will add proper date format after discussing the date input
        # if date.equals(datetime.today):
        # TODO: Change Datetime to generic
        try:
            weather = self.weatherAPI.getCurrentWeather(city=city)
        except:
            weather = "clear sky"
            #
        # if date == today:
        #     weather = self.weatherAPI.getCurrentWeather(city=city)
        # else:
        #     weather = self.weatherAPI.getFutureWeather(city=city, date=date, time=time)
        return weather


class RecommendationHelper:
    def __init__(self) -> None:
        self.searchAPIObj = utils.SearchImages()
        self.weatherHelper = WeatherHelper()

    def giveRecommendations(self, userid, gender, city=None, occasion=None, culture=None,
                            ageGroup=None, date=None, time=None):
        preferences = PreferencesHelper.givePreferences(userid, occasion)
        print(preferences)
        query_keywords = []
        weather = self.weatherHelper.getWeather(city, date, time)
        # if not preferences:
        #     query_keywords.append(gender)
        # else:
        #     for pref in preferences:
        #         query_keywords.append(pref["color"] + " " + pref["type"])
        # if not occasion:

        #     query_keywords.append(occasion)
        if gender != "":
            query_keywords.append(" gender " + gender)

        if not ageGroup:
            query_keywords.append(" for " + ageGroup)

        if not occasion:
            occasion = "regular event"
        query_keywords.append(
            "in " + weather + " weather" + " to a " + occasion)
        links = self.searchAPIObj.image_search(query_keywords, culture=culture)
        return links
