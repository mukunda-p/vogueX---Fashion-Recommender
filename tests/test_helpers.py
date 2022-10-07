import imp


import pytest
import website

from website.utils import QueryBuilder, WeatherAPI

def test_search_image_query_builder(app):
    query_key_words = ['date night', 'first anniversary']
    siObject = QueryBuilder()
    query = siObject.getQueryString(query_key_words)
    assert query == 'suggested dress for date night first anniversary '

def test_weather_api(app):
    city = 'Mumbai'
    wObj = WeatherAPI()
    weather = wObj.getCurrentWeather(city=city)
    assert True