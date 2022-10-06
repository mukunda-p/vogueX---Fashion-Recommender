import imp


import pytest
import website

from website.utils import QueryBuilder, WeatherAPI

def test_search_image_query_builder(app):
    query_key_words = ['i', 'want', 'a', 'nice', 'pizza']
    siObject = QueryBuilder()
    query = siObject.getQueryString(query_key_words)
    assert query == 'i want a nice pizza '

def test_weather_api(app):
    city = 'Mumbai'
    wObj = WeatherAPI()
    weather = wObj.getCurrentWeather(city=city)
    assert True